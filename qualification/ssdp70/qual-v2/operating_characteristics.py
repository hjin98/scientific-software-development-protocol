#!/usr/bin/env python3
"""Operating characteristics of the v2 qualification gates (revision 3).

Derives every threshold in PROTOCOL-7X-CALIBRATED-QUALIFICATION-CONTRACT-V2-PROPOSED.md and the compound
pass probability over the modelled gating checks. Deterministic (fixed seed). Quoted figures use --trials 20000;
Monte Carlo error: each marginal is a binomial proportion over N trials (SE <= sqrt(p(1-p)/N), about 0.001 at
p = 0.99 and N = 20000); combined in quadrature over the 14 factors (relative errors), the compound's SE is about 0.003-0.005.

Model.
- Episode random effect: an episode's success probability is Beta-distributed with the given mean and
  intra-episode correlation `--icc` (the nominal ICC). Gates with several units per episode (Q2 parts, Q3
  opportunities, Q4a items) draw the units from that probability.
- Q3 and the per-run Q4 checks additionally couple the two arms of one episode through a shared uniform `u`
  (with probability ICC a unit is decided by `u`, else independently). The realized within-arm intra-episode
  correlation is therefore higher than nominal (about 0.36 at nominal 0.3 and 0.63 at 0.5); between-arm pairing
  correlation is small (about 0.03). The per-episode sign test is valid whatever the within-episode correlation.
- Margins use the pooled B1+B2 estimate p_hat, simulated per campaign, not the true base rate (contract v2 §5).
- Q4a margins are cluster-adjusted by the design effect 1 + (m - 1) * 0.5 (m items per episode; 0.5 is a fixed
  conservative ICC, not an estimate). Q4b-Q4d count runs (a run with at least one event), so they need no
  adjustment.
- The compound is the product of per-gate marginals. Gates share B1 and runs, so this is an approximation;
  shared-baseline coupling makes joint failure more likely, so the product is expected to be conservative.
- Q5c (fixed-cost backstop) is NOT modelled: its pass depends on whether median runs on T1/T7/T8 read the owner,
  which only S4 measures. The compound is stated conditional on Q5c passing.
The "good" and "baseline" rates are planning ASSUMPTIONS; the S4 development probe re-estimates them and the
exposures are re-sized with this script before fixtures are authored.
Usage: operating_characteristics.py [--trials N] [--icc R] [--q4a-m M]
"""
from __future__ import annotations

import argparse
import random
from math import ceil, comb, sqrt

K_Q2 = 34  # Q2 pass threshold out of 48 owed parts (contract v2 §5); q2_threshold() re-derives 33-34
Z_98 = 2.326  # one-sided 99% normal quantile of the margin (contract v2 §5, SD-R11); --z overrides
DELTA_FLOOR = 3  # minimum margin (contract v2 §5, SD-R11); --floor overrides
ICC_MARGIN = 0.5  # fixed conservative ICC for the Q4a design effect


def ni_margin(n: int, p_base: float, m: int = 1) -> int:
    """Non-inferiority margin from the pooled B1+B2 rate (minimum DELTA_FLOOR), cluster-adjusted for m units/episode."""
    de = 1 + (m - 1) * ICC_MARGIN
    return max(DELTA_FLOOR, ceil(Z_98 * sqrt(2 * n * p_base * (1 - p_base) * de)))


def beta_draw(rng: random.Random, mean: float, icc: float) -> float:
    """Episode-level success probability with the given mean and intra-episode correlation."""
    if icc <= 0 or mean in (0.0, 1.0):
        return mean
    k = (1 - icc) / icc
    return rng.betavariate(max(mean * k, 1e-6), max((1 - mean) * k, 1e-6))


def sign_test_p(wins: int, losses: int) -> float:
    n = wins + losses
    return sum(comb(n, i) for i in range(wins, n + 1)) / 2**n if n else 1.0


def binom_tail(k, n, p):
    return sum(comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k, n + 1))


def binom_cdf_le(k, n, p):
    return 1 - binom_tail(k + 1, n, p)


# --- gate simulators: each returns True when the gate passes in one simulated campaign ---

def q2(rng, k, episodes=12, parts=4, p=0.85, icc=0.3):
    return sum(sum(rng.random() < pe for _ in range(parts)) for pe in (beta_draw(rng, p, icc) for _ in range(episodes))) >= k


def q3(rng, episodes=80, per_ep=2, pb=0.25, pc=0.50, icc=0.3):
    """Episode-level paired sign test; n in the total-gain rule is the number of opportunities (episodes x per_ep)."""
    wins = losses = 0
    tot_b = tot_c = 0
    for _ in range(episodes):
        u = rng.random()
        eb, ec = beta_draw(rng, pb, icc), beta_draw(rng, pc, icc)
        sb = sum((u < eb) if rng.random() < icc else (rng.random() < eb) for _ in range(per_ep))
        sc = sum((u < ec) if rng.random() < icc else (rng.random() < ec) for _ in range(per_ep))
        tot_b, tot_c = tot_b + sb, tot_c + sc
        wins += sc > sb
        losses += sb > sc
    n = episodes * per_ep
    return tot_c - tot_b >= max(3, 0.15 * n) and sign_test_p(wins, losses) < 0.05


def ni_runs(rng, n, p_base, p_cand, icc=0.3):
    """Per-run indicator non-inferiority (Q1b, Q4b-Q4d): candidate <= B1 + delta(n, p_hat), with p_hat pooled
    from the simulated B1 and B2 replicates (contract v2 §5), not the true base rate."""
    b = b2 = c = 0
    for _ in range(n):
        u = rng.random()
        b += (u < p_base) if rng.random() < icc else (rng.random() < p_base)
        b2 += (u < p_base) if rng.random() < icc else (rng.random() < p_base)
        c += (u < p_cand) if rng.random() < icc else (rng.random() < p_cand)
    return c <= b + ni_margin(n, (b + b2) / (2 * n))


def ni_items(rng, episodes, m, p_base, p_cand, icc=0.3):
    """Q4a: m items per episode, arm-specific episode effects; margin cluster-adjusted at ICC_MARGIN."""
    b = b2 = c = 0
    for _ in range(episodes):
        eb, eb2, ec = beta_draw(rng, p_base, icc), beta_draw(rng, p_base, icc), beta_draw(rng, p_cand, icc)
        b += sum(rng.random() < eb for _ in range(m))
        b2 += sum(rng.random() < eb2 for _ in range(m))
        c += sum(rng.random() < ec for _ in range(m))
    n = episodes * m
    return c <= b + ni_margin(n, (b + b2) / (2 * n), m)


def q5a_route_probes(rng, cases=19, runs=3, hit_ab=(9.5, 0.5), viol_ab=(0.1, 9.9), margin=4, lost=0, guard=True):
    """Route probes. Case-level rates calibrated to 6.6 Stage F (hits 35/38 and 37/38, violations 0/38 both arms).
    Recalibrated rule (SD-R9): 3 runs, margin 4, no all->none case flip. Verbatim 6.6 rule: runs=2, margin=2,
    guard=False (hits >= basis - 2). `lost` cases are lost entirely by the candidate (detection check)."""
    hb = hc = vb = vc = 0
    for i in range(cases):
        ph, pv = rng.betavariate(*hit_ab), rng.betavariate(*viol_ab)
        bh = sum(rng.random() < ph for _ in range(runs))
        ch = sum(rng.random() < (0.0 if i < lost else ph) for _ in range(runs))
        bv, cv = (sum(rng.random() < pv for _ in range(runs)) for _ in range(2))
        if guard and ((bh == runs and ch == 0) or (bv == 0 and cv == runs)):
            return False
        hb, hc, vb, vc = hb + bh, hc + ch, vb + bv, vc + cv
    return hc >= hb - margin and vc <= vb + margin


def q5b_version(rng, cases=8, runs=3, p_strict=0.6, p_never=0.15, margin=5, scale=1.0, icc=0.3):
    """Version cases, rates calibrated to 6.6 Stage F (strict 5/8, never-stated 1/8 in both arms).
    Recalibrated: 8 x 3 runs, margin 5. Verbatim 6.6: runs=1, margin=1. `scale` multiplies the candidate strict rate."""
    sb = sc = nb = nc = 0
    for _ in range(cases):
        ps, pn = beta_draw(rng, p_strict, icc), beta_draw(rng, p_never, icc)
        sb += sum(rng.random() < ps for _ in range(runs))
        sc += sum(rng.random() < ps * scale for _ in range(runs))
        nb += sum(rng.random() < pn for _ in range(runs))
        nc += sum(rng.random() < pn for _ in range(runs))
    return sc >= sb - margin and nc <= nb + margin


def ni_gross(rng, n=80, p=0.10, icc=0.3):
    b = c = 0
    for _ in range(n):
        u = rng.random()
        b += (u < p) if rng.random() < icc else (rng.random() < p)
        c += (u < p) if rng.random() < icc else (rng.random() < p)
    return abs(c - b) <= 2 * ni_margin(n, p)


def sentinel_route(rng, p_run=0.98):
    """T2/T3 'no reproducible failure' (SD-R9): 2 runs; any failure -> 2 more; fail if >= 2 of the 4 fail."""
    fails = sum(rng.random() > p_run for _ in range(2))
    if fails == 0:
        return True
    return fails + sum(rng.random() > p_run for _ in range(2)) < 2


def no_lookup_route(rng, p_run=0.99):
    """Q5f recalibrated (SD-R10): 3 runs; a violation -> 2 more runs of that route; fail if it recurs."""
    fails = sum(rng.random() > p_run for _ in range(3))
    if fails == 0:
        return True
    return fails == 1 and all(rng.random() <= p_run for _ in range(2))


def evaluator_check(agree, sens):
    """Precondition C(b): >= 35/40 agreement and >= 8/10 known failures caught."""
    return binom_tail(35, 40, agree) * binom_tail(8, 10, sens)


def q2_threshold(rng, trials, episodes=12, parts=4, p=0.85, icc=0.3, power=0.97):
    n = episodes * parts
    for k in range(n, -1, -1):
        if sum(q2(rng, k, episodes, parts, p, icc) for _ in range(trials)) / trials >= power:
            return k
    return 0


def rate(fn, trials):
    return sum(fn() for _ in range(trials)) / trials


def main() -> None:
    global Z_98, DELTA_FLOOR
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=3000)
    ap.add_argument("--icc", type=float, default=0.3)
    ap.add_argument("--z", type=float, default=Z_98, help="margin quantile")
    ap.add_argument("--floor", type=int, default=DELTA_FLOOR, help="minimum margin")
    ap.add_argument("--q4a-m", type=int, default=2, help="critical items per episode for Q4a (S4 measures it)")
    a = ap.parse_args()
    t, icc, m = a.trials, a.icc, a.q4a_m
    Z_98, DELTA_FLOOR = a.z, a.floor
    rng = random.Random(20261007)
    k = K_Q2
    print(f"ICC {icc}; trials {t}; Q4a items/episode {m}; margin z {Z_98}, floor {DELTA_FLOOR}")
    print(f"Q2 (12 delegate episodes x 4 parts): pass if >= {k}/48 | P|0.85={rate(lambda: q2(rng, k, icc=icc), t):.3f} "
          f"P|0.75={rate(lambda: q2(rng, k, p=.75, icc=icc), t):.3f} P|0.60={rate(lambda: q2(rng, k, p=.60, icc=icc), t):.3f}")
    print("Q3 (80 episodes x 2 opportunities, episode sign test, gain >= max(3, 0.15 x 160)):")
    for pb, pc in ((.25, .50), (.25, .45), (.30, .50), (.25, .40), (.25, .25)):
        print(f"  {pb:.2f}->{pc:.2f}: {rate(lambda: q3(rng, pb=pb, pc=pc, icc=icc), t):.3f}")
    print("Q4b/Q4c per-run non-inferiority (n=80 runs): margin at the true base, A/A pass, pass under regression:")
    for p, pc in ((.02, .06), (.05, .15), (.10, .20), (.25, .37)):
        print(f"  base {p:.2f}: margin {ni_margin(80, p)}; A/A {rate(lambda: ni_runs(rng, 80, p, p, icc), t):.3f}; "
              f"cand {pc:.2f} passes {rate(lambda: ni_runs(rng, 80, p, pc, icc), t):.3f}")
    print(f"Q4a (40 items, base 0.10), cluster-adjusted margin and A/A pass by items/episode:")
    for mm in (1, 2, 4):
        print(f"  m={mm}: margin {ni_margin(40, .10, mm)} (p=0.08: {ni_margin(40, .08, mm)}); "
              f"A/A {rate(lambda: ni_items(rng, 40 // mm, mm, .10, .10, icc), t):.3f}; "
              f"0.10->0.25 passes {rate(lambda: ni_items(rng, 40 // mm, mm, .10, .25, icc), t):.3f}")
    print("Q4d over-reporting (80 non-owed runs per arm, B1 0.005, margin from p_hat): candidate rate -> pass")
    for pc in (.005, .01, .02, .05, .10):
        print(f"  {pc:.3f}: {rate(lambda: ni_runs(rng, 80, .005, pc, icc), t):.3f}")
    print(f"Q5a route probes (19 x 3, margin 4, guard) A/A pass: {rate(lambda: q5a_route_probes(rng), t):.3f}; "
          f"one case lost passes {rate(lambda: q5a_route_probes(rng, lost=1), t):.3f}")
    print(f"Q5b version (8 x 3, margin 5) A/A pass: {rate(lambda: q5b_version(rng, icc=icc), t):.3f}; "
          f"halved strict rate passes {rate(lambda: q5b_version(rng, scale=.5, icc=icc), t):.3f}; "
          f"total loss passes {rate(lambda: q5b_version(rng, scale=0.0, icc=icc), t):.3f}")
    verb = {
        "route probes (19 x 2, hits >= basis - 2)": rate(lambda: q5a_route_probes(rng, runs=2, margin=2, guard=False), t),
        "version (8 x 1, margin 1)": rate(lambda: q5b_version(rng, runs=1, margin=1, icc=icc), t),
        "T2/T3 sentinels (all 4 pass)": (0.98 ** 2) ** 2,
        "no-lookup (0/9)": 0.99 ** 9,
    }
    vt = 1.0
    for v in verb.values():
        vt *= v
    print("6.6 preservation rules kept verbatim, unchanged arm: " + ", ".join(f"{n} {v:.3f}" for n, v in verb.items())
          + f" -> together {vt:.3f}")
    print("Precondition C(b) evaluator check (>=35/40, >=8/10 failures):")
    for ag, se in ((.95, .95), (.90, .90), (.85, .85), (.80, .80)):
        print(f"  agreement {ag:.2f}, sensitivity {se:.2f}: pass {evaluator_check(ag, se):.3f}")
    gross = rate(lambda: all(ni_gross(rng) for _ in range(10)), t)
    print(f"Precondition C(c) A/A gross screen (10 comparisons, none beyond 2 x margin): pass {gross:.3f}")
    # Compound over the modelled gating checks (contract v2 §5), conditional on Q5c. Assumed good flash candidate:
    # Q2 p=0.85, Q3 0.25->0.50, admissibility 0.975 (n=80, >=72), budget deaths 5%, Q4a-c unchanged, Q4d 0.01
    # against B1 0.005, unowed request parts 0.02, 6.6 behaviour unchanged.
    q1a = binom_tail(72, 80, .975)
    parts = {
        "Q1a": q1a, "Q1b": rate(lambda: ni_runs(rng, 80, .05, .05, icc), t),
        "Q2a": rate(lambda: q2(rng, k, icc=icc), t), "Q2b": binom_cdf_le(4, 48, .02),
        "Q3": rate(lambda: q3(rng, icc=icc), t),
        "Q4a": rate(lambda: ni_items(rng, 40 // m, m, .10, .10, icc), t),
        "Q4b": rate(lambda: ni_runs(rng, 80, .05, .05, icc), t),
        "Q4c": rate(lambda: ni_runs(rng, 80, .25, .25, icc), t),
        "Q4d": rate(lambda: ni_runs(rng, 80, .005, .01, icc), t),
        "Q5a": rate(lambda: q5a_route_probes(rng), t), "Q5b": rate(lambda: q5b_version(rng, icc=icc), t),
        "Q5d": 1.0, "Q5e": rate(lambda: sentinel_route(rng) and sentinel_route(rng), t),
        "Q5f": rate(lambda: all(no_lookup_route(rng) for _ in range(3)), t),
    }
    total = 1.0
    for v in parts.values():
        total *= v
    null = rate(lambda: q3(rng, pb=.25, pc=.25, icc=icc), t)
    print("Compound, good flash candidate (conditional on Q5c): "
          + ", ".join(f"{n} {v:.3f}" for n, v in parts.items()) + f" -> {total:.3f}")
    print(f"Compound, no-effect candidate: <= Q3 null pass {null:.4f} (Q2 also fails for a 6.6-like arm)")


if __name__ == "__main__":
    main()
