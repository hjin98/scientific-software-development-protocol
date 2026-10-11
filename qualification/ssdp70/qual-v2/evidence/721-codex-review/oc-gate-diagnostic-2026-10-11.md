# Operating-characteristics gate diagnostic (2026-10-11, Opus design lead)

Diagnostic only, not the frozen operating-characteristics table and not candidate evidence. Script `oc-gate-diagnostic-2026-10-11.py` (sha256 8aff1e833ccc2cdb26459805f4fe3fa62b71fbe65ebaaaa805d5ea3d88e8ef82) imports unchanged `compare_721.py` (7541b0d5...) and runs its `synthetic` + `evaluate` on the "good" scenario; 300 campaigns, 2,000 resamples (not the frozen 10,000), ICC 0.3, seed 20261011; external conditions assumed true; unresolved rates scaled relative to the 72b mimo-1 post-rerun rates.

| unresolved scale | go | not established | no-go |
|---|---:|---:|---:|
| x1.0 | 44 | 107 | 149 |
| x0.5 | 180 | 54 | 66 |
| x0.25 | 238 | 22 | 40 |
| x0 | 274 | 0 | 26 |

At x1.0: P1 FRAGILE 204/300; claim_integrity P3 harm flag at W 130/300 (detection.unnamed 28); P3 FRAGILE 44; P2 FRAGILE 16. Flags at B only 6/300.

Reading: the low go probability is caused by the W/B unresolved bracket at the historical unresolved rate (a fixed-proportion bias that more replicates do not remove), not by margins or sample size. The x1 rates come from the pre-ninth-ruling instrument whose unresolved results were mostly echo-field schema errors that p9-v2 removes by construction; the p9-v2 whole-run unresolved rate is unmeasured. Simulation draws unresolved per item independently, whereas real failures are whole-assessment; interpretation limits of the frozen table apply.
