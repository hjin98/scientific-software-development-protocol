# SSDP 7.2 qualification campaign: outcome note

**Result: NOT ESTABLISHABLE ON THIS EVIDENCE.** This is a **bounded-sensitivity** result (stakeholder eleventh ruling), **not a complete-data result**. No qualification claim is made. Candidate 7.2.0 (`2dedcfa3408f62bc11a696ac3776183a87b40438`) remains frozen, non-governing and NOT QUALIFIED; SSDP 6.6.0 remains governing.

## Data
- Executor dataset: 640 runs, complete (candidate 225, baselines 203 + 203, 6.5 reference 9; all admissible).
- Evaluator: MiMo-V2.6-Flash. Dataset `mimo-1` plus its once-only rerun `mimo-1-rerun-1`; the `mimo-2` pilot is retained as history and not used.
- Unresolved after the permitted passes: 20 runs / 60 scoring items (baseline-1 30, baseline-2 11, candidate 19). Valid dispositions are used unchanged.
- Evaluator spend about $12 in total (excluding executor and C(b)).

## Method (pre-registered)
Precondition C(c) was evaluated at 4 corner fillings plus 500 seeded random fillings (seed 20261011) of the baseline unresolved items. Candidate gates were scored at W (candidate unresolved fail, baseline unresolved pass) and B (reverse), with the same 500 fillings as a monotonicity check. Classes: ROBUST PASS (passes at W), ROBUST FAIL (fails at B), FRAGILE otherwise. A claim requires C(c) established and every required gate ROBUST PASS.

## Outcome
- C(c): established at all 504 fillings.
- ROBUST PASS (13): Q1a, Q1b, Q2a, Q2b, Q4a, Q4b, Q4c, Q5a, Q5b, Q5c, Q5d, Q5e, Q5f.
- FRAGILE (2): **Q3** (W: wins 24, losses 10, gain 12 vs 22.05 needed; B: gain 32) and **Q4d** (W: candidate 15 errors vs baseline 0, margin 3; B: 10 vs 9).
- ROBUST FAIL: none. Random fillings outside the W/B bracket: none.
- Under the claim rule, any FRAGILE gate means the result is not establishable.

## Limitations
- Single evaluator model; its unassessable-output tail (about 4% of assessments) is what leaves Q3 and Q4d open. Reruns did not converge (17 of 48 second draws failed again; the redesign pilot moved the failure tail).
- Wilson 90% intervals and per-family results under both W and B are in `bounded-sensitivity/gates.json`. A separate per-candidate-critical-error listing was not produced by this tool.
- No further evaluator pass, waiver or gate change was made; none is planned.

Records: `bounded-sensitivity/cc.json`, `gates.json`, `gates.log`; `STATUS.md`; work order §14.

## Reproducibility and review
- Command inputs: `--assessment-root evaluations/mimo-1`, `--rerun-root evaluations/mimo-1-rerun-1`, `--map` custody `operator/gate-map.json`, `--c-a` custody `operator/precondition-c-a.json`, `--c-b bounded-sensitivity/c-b-counts.json` (40/40 agree, 10/10 caught), `--static static-premeasurement.json`, attempt 2, 500 random fillings, seed 20261011. Tool sha256 `1ebc1101...`, h4 sha256 `37e8f9c2...` (full values in `gates.json`).
- Independent review of `bounded_sensitivity.py` (2026-10-11): the tool and result are sound (rule faithfully implemented, h4 and the builder remain the real owners, numbers recompute). Non-blocking notes, not changed because they cannot alter this outcome: (a) a gate passing at W but failing at B is not flagged as a bracket violation (checked against `gates.json`: no gate has W PASS and B not PASS); (b) a random filling without gate output would be skipped silently (not triggered: the same b1/b2 fillings all scored in the C(c) stage and every gate records a random status); (c) dataset roots and C(a)/C(b)/static inputs are not hashed into the tool's identity (listed above instead); (d) ROBUST PASS for the 13 gates rests on W/B plus 500 random fillings and the monotonicity assumption, not exhaustive enumeration; (e) tests do not cover `gates_stage` itself.
- Incident: while this review ran, `S4-STAKEHOLDER-RULINGS-2026-10-08.md` was found truncated to one byte by an analyst editing error at 2026-10-10 22:21 local (a write opened the file for writing before reading it), before the gates stage ran. The tool did not read the file. The file was restored from HEAD plus the seventh to eleventh sets recovered verbatim from the session transcript.

## Expected-case check (descriptive; not a gate, not a claim)
`expected_case.py` (new, unreviewed; output `bounded-sensitivity/expected-case.json`). Each of the 60 unresolved items is filled at the failure rate observed among resolved items of the same item type, either per arm (`arm`) or pooled over arms (`pooled`); 30 draws per variant, each scored with the real gates.
- Overall verdict: FAIL in 60 of 60 draws, both variants. The first failing gate is Q4d in every draw.
- **Q4d (over-reporting on non-owed runs, 90 runs):** FAIL in 60 of 60 draws. The candidate has 10 to 13 runs with an unowed null, envelope or disclosure against 0 to 1 for B1, with margin 3 to 4. Resolved data alone give candidate 10 vs baseline 0; the gate passes only if almost all of the baselines' roughly nine unresolved Q4d items were failures, against 0 failures in the baselines' resolved Q4d items. Q4d is therefore a likely failure, not merely an open question.
- **Q3 (duty composite, need gain 22.05):** per-arm rates pass in 29 of 30 draws (gain 21 to 27, median 25); pooled rates pass in 14 of 30 (gain 19 to 26, median 22). Q3 is genuinely borderline.
- All other gates pass in every draw.

## Q4d cause reading (descriptive)
Authorized read of the 10 candidate Q4d-hit final reports plus keyword counts: every hit report carries a narrated "Scientific checks" / null-envelope / variants block on a task where none was owed (4 small change-only fixes, 5 authority-document drafts, 1 D3 acceptance review). The same narration appears, less explicitly, in 37 of 80 non-hit candidate non-owed reports; B1 reports (6.6) have no such section. The 10 episodes were exposed to the analyst by this read.
