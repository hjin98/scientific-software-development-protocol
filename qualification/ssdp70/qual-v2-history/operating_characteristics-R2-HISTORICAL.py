#!/usr/bin/env python3
"""Operating characteristics of the v2 qualification gates (revision 2: cluster-aware).

Derives every threshold in PROTOCOL-7X-CALIBRATED-QUALIFICATION-CONTRACT-V2-PROPOSED.md and the compound
pass probability over all gating checks. Episodes carry random effects (intra-episode correlation ICC), so
parts and opportunities from one episode are not treated as independent. Deterministic (fixed seed).
The "good" and "baseline" rates are planning ASSUMPTIONS (see SCENARIOS); the S4 development probe
re-estimates them and the exposures are re-sized with this script before fixtures are authored.
Usage: operating_characteristics.py [--trials N] [--icc R]
"""
from __future__ import annotations

import argparse
import random
from math import ceil, comb, sqrt

K_Q2 = 34  # Q2 pass threshold out of 48 owed parts (contract v2 §4)
Z_98 = 2.054  # one-sided normal quantile for the ~98% A/A pass target of a non-inferiority check


def ni_margin(n: int, p_base: float) -> int:
    """Non-inferiority margin from the pooled A/A baseline rate (minimum 2)."""
    return max(2, ceil(Z_98 * sqrt(2 * n * p_base * (1 - p_base))))


def beta_draw(rng: random.Random, mean: float, icc: float) -> float:
    """Episode-level success probability with the given mean and intra-episode correlation."""
    if icc <= 0 or mean in (0.0, 1.0):
        return mean
    k = (1 - icc) / icc
    return rng.betavariate(max(mean * k, 1e-6), max((1 - mean) * k, 1e-6))


def sign_test_p(wins: int, losses: int) -> float:
    n = wins + losses
    return sum(comb(n, i) for i in range(wins, n + 1)) / 2**n if n else 1.0


# --- gate simulators: each returns True when the gate passes in one simulated campaign ---

def q2(rng, k, episodes=12, parts=4, p=0.85, icc=0.3):
    return sum(sum(rng.random() < pe for _ in range(parts)) for pe in (beta_draw(rng, p, icc) for _ in range(episodes))) >= k


def q3(rng, episodes=80, per_ep=2, pb=0.25, pc=0.50, icc=0.3):
    """Episode-level paired sign test on the per-episode duty score difference."""
    wins = losses = 0
    tot_b = tot_c = 0
    for _ in range(episodes):
        u = rng.random()  # shared episode difficulty couples arms and opportunities
        eb, ec = beta_draw(rng, pb, icc), beta_draw(rng, pc, icc)
        sb = sum((u < eb) if rng.random() < icc else (rng.random() < eb) for _ in range(per_ep))
        sc = sum((u < ec) if rng.random() < icc else (rng.random() < ec) for _ in range(per_ep))
        tot_b, tot_c = tot_b + sb, tot_c + sc
        wins += sc > sb
        losses += sb > sc
    n = episodes * per_ep
    return tot_c - tot_b >= max(3, 0.15 * n) and sign_test_p(wins, losses) < 0.05


def ni(rng, n, p_base, p_cand, icc=0.3):
    """Run-level count non-inferiority; paired episodes share a random effect (conservative margin)."""
    b = c = 0
    for _ in range(n):
        u = rng.random()
        b += (u < p_base) if rng.random() < icc else (rng.random() < p_base)
        c += (u < p_cand) if rng.random() < icc else (rng.random() < p_cand)
    return c <= b + ni_margin(n, p_base)


def q5a_route_probes(rng, cases=19, runs=3, hit_ab=(9.5, 0.5), viol_ab=(0.1, 9.9), margin=4, lost=0):
    # Case-level rates calibrated to 6.6 Stage F (hits 35/38 and 37/38, violations 0/38 both arms).
    """6.6 rule structure with 3 runs per case: hits >= base-margin, violations <= base+margin, no all->none case flip.
    `lost` cases are lost entirely by the candidate (detection check)."""
    hb = hc = vb = vc = 0
    for i in range(cases):
        ph, pv = rng.betavariate(*hit_ab), rng.betavariate(*viol_ab)
        bh = sum(rng.random() < ph for _ in range(runs))
        ch = sum(rng.random() < (0.0 if i < lost else ph) for _ in range(runs))
        bv, cv = (sum(rng.random() < pv for _ in range(runs)) for _ in range(2))
        if (bh == runs and ch == 0) or (bv == 0 and cv == runs):
            return False
        hb, hc, vb, vc = hb + bh, hc + ch, vb + bv, vc + cv
    return hc >= hb - margin and vc <= vb + margin


def q5b_version(rng, cases=8, runs=3, p_strict=0.6, p_never=0.15, margin=5, scale=1.0):
    # Rates calibrated to 6.6 Stage F (strict 5/8, never-stated 1/8 in both arms).
    """Aggregate strict/never-stated rule at 8 cases x 3 runs; `scale` multiplies the candidate strict rate."""
    sb = sc = nb = nc = 0
    for _ in range(cases):
        ps, pn = beta_draw(rng, p_strict, 0.3), beta_draw(rng, p_never, 0.3)
        sb += sum(rng.random() < ps for _ in range(runs))
        sc += sum(rng.random() < ps * scale for _ in range(runs))
        nb += sum(rng.random() < pn for _ in range(runs))
        nc += sum(rng.random() < pn for _ in range(runs))
    return sc >= sb - margin and nc <= nb + margin


def q5b_verbatim(rng, cases=8, p_strict=0.6, p_never=0.15):
    """6.6 rule verbatim: 8 paired episodes, strict >= base-1, never-stated <= base+1."""
    sb = sc = nb = nc = 0
    for _ in range(cases):
        ps, pn = beta_draw(rng, p_strict, 0.3), beta_draw(rng, p_never, 0.3)
        sb += rng.random() < ps; sc += rng.random() < ps
        nb += rng.random() < pn; nc += rng.random() < pn
    return sc >= sb - 1 and nc <= nb + 1


def ni_gross(rng, n=80, p=0.10, icc=0.3):
    b = c = 0
    for _ in range(n):
        u = rng.random()
        b += (u < p) if rng.random() < icc else (rng.random() < p)
        c += (u < p) if rng.random() < icc else (rng.random() < p)
    return abs(c - b) <= 2 * ni_margin(n, p)


def sentinel_route(rng, p_run=0.98):
    """T2/T3 'no reproducible failure': 2 runs; any failure -> 2 more; fail if >= 2 of the 4 fail."""
    fails = sum(rng.random() > p_run for _ in range(2))
    if fails == 0:
        return True
    return fails + sum(rng.random() > p_run for _ in range(2)) < 2


def binom_cdf_le(k, n, p):
    return 1 - binom_tail(k + 1, n, p)


def binom_tail(k, n, p):
    return sum(comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k, n + 1))


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
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=3000)
    ap.add_argument("--icc", type=float, default=0.3)
    a = ap.parse_args()
    t, icc = a.trials, a.icc
    rng = random.Random(20261007)
    k = K_Q2  # fixed; q2_threshold() re-derives it (simulation jitter puts it at 33-34)
    print(f"ICC {icc}; trials {t}")
    print(f"Q2 (12 delegate episodes x 4 parts): pass if >= {k}/48 | P|0.85={rate(lambda: q2(rng, k, icc=icc), t):.3f} "
          f"P|0.75={rate(lambda: q2(rng, k, p=.75, icc=icc), t):.3f} P|0.60={rate(lambda: q2(rng, k, p=.60, icc=icc), t):.3f}")
    print("Q3 (80 episodes x 2 opportunities, episode sign test), sensitivity to the assumed effect:")
    for pb, pc in ((.25, .50), (.25, .45), (.30, .50), (.25, .40), (.25, .25)):
        print(f"  {pb:.2f}->{pc:.2f}: {rate(lambda: q3(rng, pb=pb, pc=pc, icc=icc), t):.3f}")
    print("Q4 non-inferiority (n=80 runs): margin, A/A pass, pass under regression:")
    for p, pc in ((.02, .06), (.05, .15), (.10, .20), (.25, .37)):
        print(f"  base {p:.2f}: margin {ni_margin(80, p)}; A/A {rate(lambda: ni(rng, 80, p, p, icc), t):.3f}; "
              f"cand {pc:.2f} passes {rate(lambda: ni(rng, 80, p, pc, icc), t):.3f}")
    print(f"  Q4a at its n=40 minimum, base 0.10: margin {ni_margin(40, .10)}")
    print(f"Q5a route probes (19 x 3, margin 4) A/A pass: {rate(lambda: q5a_route_probes(rng), t):.3f}; "
          f"one case lost passes {rate(lambda: q5a_route_probes(rng, lost=1), t):.3f}")
    print(f"Q5b verbatim 6.6 rule (8 x 1, margin 1) A/A pass: {rate(lambda: q5b_verbatim(rng), t):.3f}")
    print(f"Q5b version (8 x 3, margin 5) A/A pass: {rate(lambda: q5b_version(rng), t):.3f}; "
          f"halved strict rate passes {rate(lambda: q5b_version(rng, scale=.5), t):.3f}; "
          f"total loss passes {rate(lambda: q5b_version(rng, scale=0.0), t):.3f}")
    print("Precondition C(b) evaluator check (>=35/40, >=8/10 failures):")
    for ag, se in ((.95, .95), (.90, .90), (.85, .85), (.80, .80)):
        print(f"  agreement {ag:.2f}, sensitivity {se:.2f}: pass {evaluator_check(ag, se):.3f}")
    gross = rate(lambda: all(ni_gross(rng) for _ in range(10)), t)
    print(f"Precondition C(c) A/A gross screen (10 comparisons, none beyond 2 x margin): pass {gross:.3f}")
    # Compound over every gating check (contract v2 §4). Assumed good flash candidate: Q2 p=0.85,
    # Q3 0.25->0.50, admissibility 0.975 (n=80, >=72), budget deaths 5%, Q4a-d unchanged, 6.6 behaviour unchanged.
    from math import comb as _c
    q1a = sum(_c(80, i) * .975**i * .025**(80 - i) for i in range(72, 81))
    parts = {
        "Q1a": q1a, "Q1b": rate(lambda: ni(rng, 80, .05, .05, icc), t),
        "Q2": rate(lambda: q2(rng, k, icc=icc), t), "Q3": rate(lambda: q3(rng, icc=icc), t),
        "Q4a": rate(lambda: ni(rng, 40, .10, .10, icc), t), "Q4b": rate(lambda: ni(rng, 80, .05, .05, icc), t),
        "Q4c": rate(lambda: ni(rng, 80, .25, .25, icc), t), "Q4d": rate(lambda: ni(rng, 80, .10, .10, icc), t),
        "Q5a": rate(lambda: q5a_route_probes(rng), t), "Q5b": rate(lambda: q5b_version(rng), t),
        "Q5c": 0.99, "Q5d static": 1.0, "T2/T3 sentinels": rate(lambda: sentinel_route(rng) and sentinel_route(rng), t),
        "Q2b unowed parts <= 4": binom_cdf_le(4, 48, .02),
        "Q5f no-lookup (reproducible)": rate(lambda: all(sentinel_route(rng, .99) for _ in range(9)), t),
    }
    total = 1.0
    for v in parts.values():
        total *= v
    null = rate(lambda: q3(rng, pb=.25, pc=.25, icc=icc), t)
    print("Compound, good flash candidate: " + ", ".join(f"{n} {v:.3f}" for n, v in parts.items()) + f" -> {total:.3f}")
    print(f"Compound, no-effect candidate: <= Q3 null pass {null:.3f} (Q2 also fails for a 6.6-like arm)")


if __name__ == "__main__":
    main()
