"""Diagnostic only: which gate of the frozen evaluate() blocks synthetic campaigns. Imports compare_721 unchanged; not a frozen-parameter result."""
import sys, math, collections
sys.path.insert(0, sys.argv[1])
import numpy as np, compare_721 as c
reps, B = int(sys.argv[2]), int(sys.argv[3])
for scale in map(float, sys.argv[4].split(",")):
    for name in [n for n in c.SIM_SCENARIOS if n.startswith("good:")]:
        rng = np.random.default_rng(c.SEED)
        icc = 0.3; sigma = math.sqrt(icc/(1-icc)*math.pi**2/3)
        asg = {i: np.sort(rng.permutation(c.DESIGN_EPISODES)[:c.DESIGN[i][0]]) for i in c.DESIGN}
        for g in ["delegate_request.R","delegate_request.T","delegate_request.V","delegated_finding_loss"]: asg[g]=asg["delegate_request.F"]
        cal = {}
        for i,(_,r,_) in c.DESIGN.items():
            for rr in {r, c.SIM_SCENARIOS[name].get(i,r)}: cal[(i,rr)] = c.calibrate(rr, sigma)
        cnt = collections.Counter(); out = collections.Counter()
        for _ in range(reps):
            t = c.synthetic(rng, c.SIM_SCENARIOS[name], icc, asg, cal, scale)
            idx = rng.integers(0, c.DESIGN_EPISODES, size=(B, c.DESIGN_EPISODES))
            r = c.evaluate(t, c.DESIGN_EPISODES, idx)
            out[r["statistical_outcome"]] += 1
            for p,k in r["classes"].items():
                if k != "PASS": cnt[f"{p} {k}"] += 1
            for f in {(f["flag"], f["item"], f["scenario"]) for f in r["flags"]}: cnt[f"flag {f}"] += 1
            if any(f["scenario"]=="B" for f in r["flags"]): cnt["any flag at B"] += 1
            if any(f["scenario"]=="W" for f in r["flags"]): cnt["any flag at W"] += 1
        print(f"\n== unresolved x{scale} | {name} | reps {reps} B {B}: {dict(out)}")
        for k,v in cnt.most_common(): print(f"  {v:4d}  {k}")
