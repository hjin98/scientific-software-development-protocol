operating characteristics: decision function evaluate() on synthetic episode-clustered data; 300 simulated campaigns per scenario, 10000 bootstrap resamples each, ICC 0.3 (latent logit scale), unresolved rates x1.0 of the 72b observed ones, seed 20261011; external conditions assumed to hold; aa at the 72b p72 rates
| scenario | go probability | outcomes |
|---|---|---|
| good: narration cut to 2%, otherwise neutral | 0.13 | {"go": 39, "no-go": 168, "not established": 93} |
| narration cut only to 5% | 0.03 | {"go": 8, "no-go": 168, "not established": 124} |
| narration not reduced | 0.00 | {"no-go": 250, "not established": 50} |
| good + delegated_finding_loss back to the 6.6 level (3/14) | 0.05 | {"go": 16, "no-go": 245, "not established": 39} |
| good + tension_report back to the 6.6 level (17/26) | 0.04 | {"go": 13, "no-go": 246, "not established": 41} |
| good + detection.unnamed 68% -> 85% | 0.02 | {"go": 7, "no-go": 282, "not established": 11} |
| good + claim_integrity 8% -> 20% | 0.00 | {"go": 1, "no-go": 299} |
| good + o1_authoring lost entirely (100%) | 0.00 | {"no-go": 300} |
| good + delegate_request.F/R/T/V back to the 6.6 level | 0.00 | {"no-go": 300} |
