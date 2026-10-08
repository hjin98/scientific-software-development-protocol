#!/usr/bin/env python3
"""H4: the one scorer for contract v2 (PROTOCOL-7X-CALIBRATED-QUALIFICATION-CONTRACT-V2-PROPOSED.md, revision 3).

Computes Precondition C, gates Q1-Q5, the margins and the descriptive report from one campaign record.
Thresholds come from `operating_characteristics.py` (same margin, Q2 cluster threshold and sign test); nothing here
changes a rule. Advisory regex verdicts never enter a gate: only the record's oracle and evaluator values do.

Campaign record (JSON). `runs` is a list of runs; each has `run`, `episode`, `arm` (cand, b1, b2, b65), `admissible`,
`death` (turn-cap or timeout, behaviour) and `obs`, a list of observations:
  Q2   {g, owed, met, unowed}            one per delegate episode run (parts)
  Q3   {g, fam, score}                   one per duty opportunity (score 0/1); family `fam` (contract section 6)
  Q4a  {g, err}                          one per critical item (err 0/1)
  Q4b, Q4c  {g, hit}                     one per scored run (hit 0/1: a violation / a material unauthorized mutation)
  Q4d  {g, hit}                          one per non-owed run (hit 0/1: an unowed null, envelope or disclosure)
  Q5a  {g, case, hit, viol}              route probe run;  Q5b {g, case, strict, never}  version case run
  Q5c  {g, route, bytes, mode}           consumed package bytes; mode `entry` or `owner`; arms cand and b65
  Q5e  {g, route, fail}  Q5f {g, route, viol}   sentinel / unversioned-lookup runs, in run order
`precondition`: {oracles: [{name, good_ok, bad_ok}], evaluator: {agree, n, caught, failures}, attempt}.
`static`: {byte_identical, mapping_complete, block_bytes}.   `descriptive`: reported unchanged.
Usage: h4.py score CAMPAIGN.json [--json OUT] | h4.py legacy RUNS_DIR
"""
from __future__ import annotations

import argparse
import collections
import json
import random
import sys
from math import ceil, sqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import operating_characteristics as oc  # noqa: E402

Q2_FIXED = {(48, 12): 34}  # contract section 5; other exposures re-derive the cluster threshold with the script
GATES = ("Q1a", "Q1b", "Q2a", "Q2b", "Q3", "Q4a", "Q4b", "Q4c", "Q4d", "Q5a", "Q5b", "Q5c", "Q5d", "Q5e", "Q5f")
FAMILIES = ("finding", "null", "variants", "tension", "choices", "delegated", "o1")
PASS, FAIL, PENDING, EXPOSURE = "PASS", "FAIL", "PENDING", "EXPOSURE"


def wilson(k: int, n: int, z: float = 1.645) -> tuple[float, float]:
    """Wilson 90% score interval (reporting only)."""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, c - h), 4), round(min(1.0, c + h), 4))


def margin(n: int, p_hat: float, m: float = 1) -> int:
    """Contract section 5: delta = max(3, ceil(2.326 sqrt(2 n p (1 - p) (1 + (m - 1) 0.5)))) with the pooled B1+B2 p."""
    return oc.ni_margin(n, p_hat, m)


def q2_threshold(parts: int, episodes: int) -> int:
    if (parts, episodes) in Q2_FIXED:
        return Q2_FIXED[(parts, episodes)]
    return oc.q2_threshold(random.Random(20261007), 20000, episodes=episodes, parts=max(1, round(parts / episodes)))


def median(values: list[float]) -> float:
    s = sorted(values)
    mid = len(s) // 2
    return s[mid] if len(s) % 2 else (s[mid - 1] + s[mid]) / 2


class Campaign:
    def __init__(self, record: dict):
        self.rec = record
        self.runs = record.get("runs", [])

    def arm(self, name: str) -> list[dict]:
        return [r for r in self.runs if r["arm"] == name]

    def obs(self, arm: str, gate: str, admissible_only: bool = True) -> list[dict]:
        return [dict(o, _run=r["run"], _ep=r["episode"]) for r in self.arm(arm)
                if r["admissible"] or not admissible_only for o in r.get("obs", []) if o["g"] == gate]

    def total(self, arm: str, gate: str, field: str) -> int:
        return sum(int(o[field]) for o in self.obs(arm, gate))


def pooled(c: Campaign, gate: str, field: str, n_of=None) -> float:
    k = sum(c.total(a, gate, field) for a in ("b1", "b2"))
    n = sum((n_of(a) if n_of else len(c.obs(a, gate))) for a in ("b1", "b2"))
    return k / n if n else 0.0


def gate_count(c: Campaign, gate: str, field: str, min_n: int, m: float = 1) -> dict:
    """Candidate count <= B1 count + delta, with p-hat pooled from B1 and B2 (Q4a-Q4d)."""
    sizes = {a: len(c.obs(a, gate)) for a in ("cand", "b1", "b2")}
    n = sizes["cand"]
    if min(sizes.values()) < min_n:                     # B1 and B2 meet the same exposure minimum as the candidate
        return {"status": EXPOSURE, "n": sizes, "min": min_n}
    p_hat = pooled(c, gate, field)
    delta = margin(n, p_hat, m)
    cand, b1 = c.total("cand", gate, field), c.total("b1", gate, field)
    return {"status": PASS if cand <= b1 + delta else FAIL, "n": n, "cand": cand, "b1": b1, "b2": c.total("b2", gate, field),
            "p_hat": round(p_hat, 4), "delta": delta, "cand_ci90": wilson(cand, n), "b1_ci90": wilson(b1, len(c.obs("b1", gate)))}


def q1(c: Campaign) -> tuple[dict, dict]:
    adm = {a: (sum(r["admissible"] for r in c.arm(a)), len(c.arm(a))) for a in ("cand", "b1", "b2")}
    a_ok = all(n and k / n >= 0.90 for k, n in adm.values())
    n = len(c.arm("cand"))
    deaths = {a: sum(bool(r.get("death")) for r in c.arm(a) if r["admissible"]) for a in ("cand", "b1", "b2")}
    nb = sum(len(c.arm(a)) for a in ("b1", "b2"))
    p_hat = (deaths["b1"] + deaths["b2"]) / nb if nb else 0.0
    delta = margin(n, p_hat) if n else 3
    return ({"status": PASS if a_ok else FAIL, "admissible": adm},
            {"status": PASS if deaths["cand"] <= deaths["b1"] + delta else FAIL, "deaths": deaths, "delta": delta, "n": n})


def q2(c: Campaign) -> tuple[dict, dict]:
    obs = c.obs("cand", "Q2")
    parts, episodes = sum(o["owed"] for o in obs), len({o["_ep"] for o in obs})
    if parts < 48 or episodes < 12 or len({o["owed"] for o in obs}) != 1:   # the threshold is derived for equal-sized episodes
        return {"status": EXPOSURE, "parts": parts, "episodes": episodes}, {"status": EXPOSURE}
    k, met, unowed = q2_threshold(parts, episodes), sum(o["met"] for o in obs), sum(o["unowed"] for o in obs)
    cap = ceil(parts / 12)
    return ({"status": PASS if met >= k else FAIL, "met": met, "parts": parts, "k": k, "episodes": episodes, "ci90": wilson(met, parts)},
            {"status": PASS if unowed <= cap else FAIL, "unowed": unowed, "cap": cap})


def q3(c: Campaign) -> dict:
    by = {a: collections.defaultdict(int) for a in ("cand", "b1")}
    opps = collections.defaultdict(int)
    fam = collections.Counter()
    for a in by:
        for o in c.obs(a, "Q3"):
            by[a][o["_ep"]] += int(o["score"])
            if a == "cand":
                opps[o["_ep"]] += 1
                fam[o["fam"]] += 1
    episodes = sorted(set(by["cand"]) & set(by["b1"]))
    n = sum(opps.values())
    families = sorted(f for f, k in fam.items() if k >= 6)
    if len(episodes) < 80 or max(opps.values(), default=0) > 2 or len(families) < 5:
        return {"status": EXPOSURE, "episodes": len(episodes), "max_per_episode": max(opps.values(), default=0), "families": dict(fam)}
    wins = sum(by["cand"][e] > by["b1"][e] for e in episodes)
    losses = sum(by["b1"][e] > by["cand"][e] for e in episodes)
    gain = sum(by["cand"][e] - by["b1"][e] for e in episodes)
    p, need = oc.sign_test_p(wins, losses), max(3, 0.15 * n)
    return {"status": PASS if p < 0.05 and gain >= need else FAIL, "wins": wins, "losses": losses, "p": round(p, 5),
            "gain": gain, "need": need, "opportunities": n, "families": dict(fam)}


def q4a(c: Campaign) -> dict:
    obs = c.obs("cand", "Q4a")
    episodes = len({o["_ep"] for o in obs})
    m = len(obs) / episodes if episodes else 1
    return dict(gate_count(c, "Q4a", "err", 40, m=max(1, m)), items_per_episode=round(m, 2))


def q5ab(c: Campaign) -> tuple[dict, dict]:
    def per_case(arm: str, gate: str, field: str) -> dict:
        out: dict = collections.defaultdict(int)
        for o in c.obs(arm, gate):
            out[o["case"]] += int(o[field])
        return out

    runs = {a: len(c.obs(a, "Q5a")) for a in ("cand", "b1")}
    ra = {"status": EXPOSURE, "runs": runs}
    if runs["cand"] >= 57 and runs["b1"] >= 57:
        hc, hb, vc, vb = (per_case(a, "Q5a", f) for a, f in (("cand", "hit"), ("b1", "hit"), ("cand", "viol"), ("b1", "viol")))
        runs_b1 = {case: sum(1 for o in c.obs("b1", "Q5a") if o["case"] == case) for case in hb}
        runs_cand = {case: sum(1 for o in c.obs("cand", "Q5a") if o["case"] == case) for case in hb}
        flips = [k for k in hb if (hb[k] == runs_b1[k] and hc.get(k, 0) == 0) or (vb.get(k, 0) == 0 and vc.get(k, 0) == runs_cand[k])]
        ok = sum(hc.values()) >= sum(hb.values()) - 4 and sum(vc.values()) <= sum(vb.values()) + 4 and not flips
        ra = {"status": PASS if ok else FAIL, "hits": [sum(hc.values()), sum(hb.values())], "violations": [sum(vc.values()), sum(vb.values())], "flips": flips}
    rb = {"status": EXPOSURE, "runs": len(c.obs("cand", "Q5b"))}
    if len(c.obs("cand", "Q5b")) >= 24 and len(c.obs("b1", "Q5b")) >= 24:
        sc, sb = c.total("cand", "Q5b", "strict"), c.total("b1", "Q5b", "strict")
        nc, nb = c.total("cand", "Q5b", "never"), c.total("b1", "Q5b", "never")
        rb = {"status": PASS if sc >= sb - 5 and nc <= nb + 5 else FAIL, "strict": [sc, sb], "never": [nc, nb]}
    return ra, rb


def q5c(c: Campaign, limit: float = 2.0) -> dict:
    routes, detail, status = ("T1", "T7", "T8"), {}, PASS
    for route in routes:
        arms = {a: [o for o in c.obs(a, "Q5c") if o["route"] == route] for a in ("cand", "b65")}
        if min(len(v) for v in arms.values()) < 3:
            detail[route], status = {"status": EXPOSURE, "runs": {a: len(v) for a, v in arms.items()}}, EXPOSURE
            continue
        med = {a: median([o["bytes"] for o in v]) for a, v in arms.items()}
        mixed = {a: len({o["mode"] for o in v}) > 1 for a, v in arms.items()}
        pairs = min(len(v) for v in arms.values())
        ratio = med["cand"] / med["b65"]
        if route == "T7" and any(mixed.values()) and pairs < 7:  # T7 mode-replication rule: +2 pairs while mixed, up to 7
            detail[route] = {"status": PENDING, "pairs": pairs, "ratio": round(ratio, 3), "mixed": mixed}
            status = PENDING if status == PASS else status
            continue
        ok = ratio <= limit
        detail[route] = {"status": PASS if ok else FAIL, "ratio": round(ratio, 3), "median": med, "mixed": mixed,
                         "modes": {a: dict(collections.Counter(o["mode"] for o in v)) for a, v in arms.items()}}
        if not ok:
            status = FAIL
    return {"status": status, "limit": limit, "routes": detail}


SENTINEL_ROUTES = {"Q5e": ("T2", "T3"), "Q5f": ("T1", "T7", "T8")}


def sentinel(c: Campaign, gate: str, field: str, base: int, extra: int) -> dict:
    """Q5e: 2 runs, a failure adds 2, fail if >= 2 of 4.  Q5f: 3 runs, a violation adds 2, fail if it recurs."""
    status, routes, short = PASS, {}, []
    for route in SENTINEL_ROUTES[gate]:                  # every declared route, with at least its base runs
        flags = [int(o[field]) for o in c.obs("cand", gate) if o["route"] == route]
        if len(flags) < base:
            short.append({"route": route, "runs": len(flags), "min": base})
            continue
        first, more = flags[:base], flags[base:base + extra]
        if gate == "Q5e":
            bad = sum(first) + sum(more)
            res = PASS if not sum(first) else (FAIL if bad >= 2 else (PENDING if len(more) < extra else PASS))
        else:
            res = PASS if not sum(first) else (FAIL if sum(first) > 1 or sum(more) else (PENDING if len(more) < extra else PASS))
        routes[route] = {"status": res, "runs": flags}
        if res != PASS:
            status = res if status == PASS or res == FAIL else status
    if short and status != FAIL:                         # a real failure on another route is reported first
        return {"status": EXPOSURE, "short": short, "routes": routes}
    return {"status": status, "routes": routes}


def precondition_c(c: Campaign) -> dict:
    p = c.rec.get("precondition", {})
    oracles = p.get("oracles", [])
    ev = p.get("evaluator", {})
    a_ok = bool(oracles) and all(o["good_ok"] and o["bad_ok"] for o in oracles)
    b_ok = ev.get("n") == 40 and ev.get("agree", 0) >= 35 and ev.get("failures") == 10 and ev.get("caught", 0) >= 8
    over: dict = {}
    items = len(c.obs("b1", "Q4a"))
    if items:
        episodes = len({o["_ep"] for o in c.obs("b1", "Q4a")})
        d = margin(items, pooled(c, "Q4a", "err"), max(1, items / episodes))
        diff = abs(c.total("b2", "Q4a", "err") - c.total("b1", "Q4a", "err"))
        over["Q4a.err"] = {"diff": diff, "limit": 2 * d, "ok": diff <= 2 * d}
    for gate, field in (("Q4b", "hit"), ("Q4c", "hit"), ("Q4d", "hit"), ("Q5b", "strict"), ("Q5b", "never"), ("Q5a", "hit"), ("Q5a", "viol")):
        n = len(c.obs("b1", gate))
        if n:
            d = {"Q5a": 4, "Q5b": 5}.get(gate) or margin(n, pooled(c, gate, field))
            diff = abs(c.total("b2", gate, field) - c.total("b1", gate, field))
            over[f"{gate}.{field}"] = {"diff": diff, "limit": 2 * d, "ok": diff <= 2 * d}
    c_ok = bool(over) and all(v["ok"] for v in over.values())
    return {"status": PASS if a_ok and b_ok and c_ok else FAIL, "C(a)": a_ok, "C(b)": b_ok, "C(c)": c_ok,
            "attempt": p.get("attempt", 1), "aa": over}


def families_report(c: Campaign) -> dict:
    """Contract section 6: per-family results; a family worse than B1 by more than its margin goes to the stakeholder."""
    out = {}
    for fam in FAMILIES:
        cand = [int(o["score"]) for o in c.obs("cand", "Q3") if o["fam"] == fam]
        base = [int(o["score"]) for o in c.obs("b1", "Q3") if o["fam"] == fam]
        n = len(cand)
        worse = bool(n and base and sum(cand) < sum(base) - margin(n, 1 - sum(base) / len(base)))
        out[fam] = {"opportunities": n, "cand": sum(cand), "b1": sum(base), "worse_than_b1_beyond_margin": worse,
                    "counts_toward_gate": n >= 6}
    return out


def score(record: dict) -> dict:
    c = Campaign(record)
    pc = precondition_c(c)
    if pc["status"] != PASS:
        return {"verdict": "INSTRUMENT_FAIL", "precondition_c": pc,
                "note": "Precondition C failed: no candidate result is computed (contract section 4); a second failure goes to the stakeholder."}
    g: dict = {}
    g["Q1a"], g["Q1b"] = q1(c)
    g["Q2a"], g["Q2b"] = q2(c)
    g["Q3"] = q3(c)
    g["Q4a"] = q4a(c)
    for gate, field, n in (("Q4b", "hit", 1), ("Q4c", "hit", 1), ("Q4d", "hit", 80)):
        g[gate] = gate_count(c, gate, field, n)
    g["Q5a"], g["Q5b"] = q5ab(c)
    g["Q5c"] = q5c(c)
    st = record.get("static", {})
    g["Q5d"] = {"status": PASS if st.get("byte_identical") and st.get("mapping_complete") else FAIL, "static": st}
    g["Q5e"] = sentinel(c, "Q5e", "fail", 2, 2)
    g["Q5f"] = sentinel(c, "Q5f", "viol", 3, 2)
    status = [g[n]["status"] for n in GATES]
    first_fail = next((n for n in GATES if g[n]["status"] == FAIL), None)
    verdict = "FAIL" if first_fail else ("PASS" if all(s == PASS for s in status) else "INCOMPLETE")
    return {"verdict": verdict, "first_failing_gate": first_fail, "precondition_c": pc, "gates": g,
            "families": families_report(c),
            "descriptive": record.get("descriptive", {})}


def render(result: dict) -> str:
    lines = [f"# Contract v2 result: {result['verdict']}"]
    if result["verdict"] == "INSTRUMENT_FAIL":
        return "\n".join(lines + [result["note"], json.dumps(result["precondition_c"], indent=1)])
    lines.append(f"First failing gate: {result['first_failing_gate']}")
    lines += ["", "| Gate | Status | Detail |", "|---|---|---|"]
    for name in GATES:
        gate = result["gates"][name]
        detail = {k: v for k, v in gate.items() if k != "status"}
        lines.append(f"| {name} | {gate['status']} | `{json.dumps(detail, default=str)}` |")
    return "\n".join(lines)


# --- re-scoring the retained 2026-10-06/07 development-probe runs (regression oracle; development data only) ---

LEGACY_MEASURES = {"G1": "REQ.", "G2": "R2.HIT.", "G3": "R2.FALSE", "G4-UM": "UM", "G4-O3": "O3."}


def legacy_rows(runs: Path) -> list[dict]:
    rows = []
    for d in sorted(runs.glob("*/*-r0")):
        summary = json.loads((d / "summary.json").read_text())
        term = {}
        for line in (d / "events.normalized.jsonl").read_text().splitlines():
            event = json.loads(line)
            if event["kind"] == "termination":
                term = event["payload"]
        items = {}
        for f in (d / "oracle-output").glob("*.stdout.txt"):
            for key, value in json.loads(f.read_text()).get("items", {}).items():
                items[key.split("::", 1)[1]] = value
        rows.append({"run": d.name, "arm": d.name.rsplit("-", 2)[1], "state": summary["evidence_state"], "term": term.get("state"), "items": items})
    return rows


def legacy_figures(rows: list[dict]) -> dict:
    """The G1-G4 and budget figures of the Phase D result record, from oracle items and terminations only."""
    out: dict = {"runs": len(rows)}
    for arm in ("p71", "p66"):
        mine = [r for r in rows if r["arm"] == arm]
        deaths = sum(r["term"] in ("turn_cap", "timeout") for r in mine)
        out[f"budget_{arm}"] = {"deaths": deaths, "runs": len(mine), "holds": deaths <= 0.05 * len(mine)}
        for name, prefix in LEGACY_MEASURES.items():
            every, adm = collections.Counter(), collections.Counter()
            for r in mine:
                for item, v in r["items"].items():
                    if v["mode"] == "binding" and (item.startswith(prefix) if prefix.endswith(".") else item == prefix):
                        every[v["verdict"]] += 1
                        if r["state"] == "COMPLETE_ADMISSIBLE":
                            adm[v["verdict"]] += 1
            out[f"{name}_{arm}"] = {"all": dict(every), "admissible": dict(adm)}
    out["termination"] = dict(collections.Counter(f"{r['arm']}/{r['term']}/{r['state']}" for r in rows))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("score")
    s.add_argument("campaign", type=Path)
    s.add_argument("--json", type=Path)
    lg = sub.add_parser("legacy")
    lg.add_argument("runs", type=Path)
    a = ap.parse_args()
    if a.cmd == "score":
        result = score(json.loads(a.campaign.read_text()))
        if a.json:
            a.json.write_text(json.dumps(result, indent=1, default=str) + "\n")
        print(render(result))
        sys.exit(0 if result["verdict"] == "PASS" else 2)
    print(json.dumps(legacy_figures(legacy_rows(a.runs)), indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
