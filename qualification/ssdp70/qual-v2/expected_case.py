#!/usr/bin/env python3
"""Expected-case DESCRIPTIVE check for the unresolved assessments (follows bounded_sensitivity.py; offline, no provider call).

Each unresolved item is filled with a random disposition drawn at the failure rate observed among the RESOLVED items of the same item type
(the part of the key before the first "."): either per arm (`arm`) or pooled over the three arms (`pooled`). Every filling is scored with
the real gates (`h4.score`). This is not a gate and not a claim; it shows where a realistic filling lands between the bracket W (worst) and
B (best). Every output is labelled descriptive.

  expected_case.py WORK --map M --c-a A --c-b B --static S --assessment-root P [--rerun-root R] --out-dir D [--draws 30]
"""
from __future__ import annotations

import argparse
import collections
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bounded_sensitivity as bs  # noqa: E402
import h4  # noqa: E402

LABEL = "DESCRIPTIVE expected-case check (not a gate, not a claim; follows the bounded-sensitivity result)"
SEED = 20261012


def item_type(key: str) -> str:
    return key.split("::", 1)[1].split(".", 1)[0]


def rates(an, by_arm: bool):
    record = json.loads((an.scratch / "base-record.json").read_text())
    arm_of = {r["run"]: r["arm"] for r in record["runs"]}
    n, f = collections.Counter(), collections.Counter()
    for key, disp in an.base.items():
        run = key.split("::", 1)[0]
        arm = arm_of.get(run)
        if arm not in bs.ARMS:
            continue
        k = (arm if by_arm else "all", item_type(key))
        n[k] += 1
        f[k] += disp == "fail"
    return n, f


def chooser(an, by_arm: bool, n, f, seed: str):
    arm_n, arm_f = collections.Counter(), collections.Counter()
    for (arm, _), c in n.items():
        arm_n[arm] += c
        arm_f[arm] += f[(arm, _)]

    def choose(arm, key):
        a = arm if by_arm else "all"
        t = (a, item_type(key))
        p = f[t] / n[t] if n[t] else (arm_f[a] / arm_n[a] if arm_n[a] else 0.5)
        return "fail" if random.Random(f"{seed}:{key}").random() < p else "pass"
    return choose


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("work", type=Path)
    for name in ("map", "c-a", "c-b", "static", "assessment-root", "out-dir"):
        ap.add_argument(f"--{name}", type=Path, required=True)
    ap.add_argument("--rerun-root", type=Path)
    ap.add_argument("--panels", nargs="+", default=["main", "versioning", "sentinels", "sentinels-add"])
    ap.add_argument("--attempt", type=int, default=2)
    ap.add_argument("--draws", type=int, default=30)
    ap.add_argument("--random", type=int, default=0)
    a = ap.parse_args(argv)
    a.out_dir.mkdir(parents=True, exist_ok=True)
    an = bs.Analysis(a).load_base()
    out = {"label": LABEL, "identity": an.identity(), "draws": a.draws, "seed": SEED, "variants": {}}
    for by_arm in (True, False):
        name = "arm" if by_arm else "pooled"
        n, f = rates(an, by_arm)
        rows = []
        for i in range(a.draws):
            res = h4.score(an.record_for(chooser(an, by_arm, n, f, f"{SEED}:{name}:{i}")))
            gates = res.get("gates", {})
            rows.append({"verdict": res.get("verdict"), "first_failing_gate": res.get("first_failing_gate"),
                         "status": {g: v["status"] for g, v in gates.items()},
                         "q3": {k: gates["Q3"].get(k) for k in ("wins", "losses", "gain", "need")} if "Q3" in gates else None,
                         "q4d": {k: gates["Q4d"].get(k) for k in ("cand", "b1", "b2", "delta")} if "Q4d" in gates else None})
        per_gate = {g: collections.Counter(r["status"].get(g) for r in rows) for g in rows[0]["status"]}
        out["variants"][name] = {"verdicts": collections.Counter(r["verdict"] for r in rows),
                                 "gate_status_counts": {g: dict(c) for g, c in per_gate.items() if set(c) != {"PASS"}},
                                 "gates_always_pass": sorted(g for g, c in per_gate.items() if set(c) == {"PASS"}),
                                 "q3": [r["q3"] for r in rows], "q4d": [r["q4d"] for r in rows]}
        print(name, json.dumps({k: out["variants"][name][k] for k in ("verdicts", "gate_status_counts")}, default=dict), flush=True)
    (a.out_dir / "expected-case.json").write_text(json.dumps(out, indent=1, default=dict) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
