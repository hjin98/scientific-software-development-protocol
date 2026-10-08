#!/usr/bin/env python3
"""Campaign-record builder: run directories -> the `h4.py score` input, with a slot and integrity audit.

Analyst tool (campaign work order gap 4, and gap 2 for declared slots). It changes no gate, threshold or margin and reads only
run directories, a slot declaration and a gate map. It never opens custody stores, keys or oracle sources: it reads
`summary.json`, `requirements-snapshot.json` (item id, measure, critical), `oracle-output/*.stdout.txt` (item verdicts) and
`events.normalized.jsonl` (termination) from each run.

It fails closed: nothing is defaulted. The gate map is required, every mapped measure must match an item, an item with no
resolved verdict blocks scoring (exit 4), and unchecked integrity inputs are findings.

Declaration (JSON):
  {"slots": [{"episode": "EP-001", "arm": "cand", "replicate": 0, "non_owed": false, "scored": true}, ...],
   "arms": {"cand": "p72", "b1": "p66", "b2": "p66b", "b65": "p65"},        # h4 label -> run-name arm key (must be one-to-one)
   "q5c_routes": ["T1", "T7", "T8"],         # slots on these routes yield Q5c only (no Q2-Q4 observations) unless "scored": true
   "execution_mode": "qualification", "purpose": "qualification",             # required run fields (summary.execution_mode, accounting.purpose)
   "profile_key_sha256": "...",                                                # required unless "unchecked_profile": true
   "no_activation_arms": [],                                                   # run-name arm keys exempt from deterministic activation
   "check_pair_order": true,                                                   # audit summary.pair_order and alternation
   "infra_error_patterns": ["\\\\b(429|5\\\\d\\\\d)\\\\b", "connection", "ECONN"]}  # provider-transport causes of an infrastructure failure
  `non_owed` (custodian-declared): the run owed no delegate request; it is the Q4d population. The builder does not infer it.
Gate map (JSON, required): {"q2_owed": [measures], "q2_unowed": {"measures": [...], "id_prefixes": [...]},
  "q3": {"measure": "family"}, "q4b": [measures], "q4c": [measures], "q4d": {"measures": [...], "id_prefixes": [...]}}
Verdicts: a binding oracle verdict decides. An advisory verdict is unadjudicated and is NOT used, unless a disposition for
(run, item) is supplied with --dispositions ({"<run>::<item>": "pass"|"fail"}). `--dev-advisory-as-evaluator` treats advisory
verdicts as dispositions for development cross-checks only and labels the record.

Admissibility (contract section 3): COMPLETE_ADMISSIBLE is admissible; EXECUTION_ERROR whose termination is turn_cap or timeout
is behaviour (admissible, death). Another EXECUTION_ERROR is infrastructure only if its error message matches an infra pattern;
it may be rerun once. Originals come from --runs, reruns from --rerun; both identities are kept; a second failure is
inadmissible; a rerun of a slot whose original was not infrastructure is an INTEGRITY finding.

Usage: build_campaign_record.py --declaration D.json --map M.json --runs DIR [--runs DIR ...] [--rerun DIR ...]
         [--dispositions F.json] [--subject-commit ARMKEY=COMMIT ...] [--allow-unchecked-subject] [--allow-unresolved]
         [--out CAMPAIGN.json] [--audit AUDIT.json]
Exit: 0 clean; 3 INTEGRITY finding; 4 unresolved items only (no INTEGRITY).
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

SCORABLE = {"pass": 1, "fail": 0}
DEFAULT_INFRA = [r"\b(429|5\d\d)\b", r"connection", r"ECONN"]


def termination(run: Path) -> dict:
    p = run / "events.normalized.jsonl"
    if p.exists():
        for line in p.read_text().splitlines():
            event = json.loads(line)
            if event.get("kind") == "termination":
                return event["payload"]
    return {}


def classify(run: Path, infra_patterns: list[str]) -> dict:
    s = json.loads((run / "summary.json").read_text())
    state, term = s["evidence_state"], termination(run)
    message = str((term.get("native_return_state") or {}).get("errorMessage", ""))
    if state == "COMPLETE_ADMISSIBLE":
        kind = "ok"
    elif state == "EXECUTION_ERROR" and term.get("state") in ("turn_cap", "timeout"):
        kind = "death"
    elif state == "EXECUTION_ERROR" and any(re.search(p, message) for p in infra_patterns):
        kind = "infra"
    else:
        kind = "malformed"
    return {"summary": s, "state": state, "term": term.get("state"), "kind": kind, "dir": str(run), "name": run.name}


def items_of(run: Path) -> dict:
    manifest = {i["id"].split("::", 1)[-1]: i for i in json.loads((run / "requirements-snapshot.json").read_text())["expected_scoring_items"]}
    verdicts = {}
    for f in sorted((run / "oracle-output").glob("*.stdout.txt")):
        text = f.read_text().strip()
        if not text:                                       # an oracle that prints nothing leaves its items unresolved
            continue
        for key, value in json.loads(text).get("items", {}).items():
            verdicts[key.split("::", 1)[-1]] = value
    return {k: dict(m, oracle=verdicts.get(k)) for k, m in manifest.items()}


def matches(k: str, m: dict, spec: dict) -> bool:
    return m["measure"] in spec.get("measures", []) or any(k.startswith(p) for p in spec.get("id_prefixes", []))


def mapped_specs(gmap: dict) -> list[dict]:
    flat = lambda ms: {"measures": list(ms)}  # noqa: E731
    return [flat(gmap["q2_owed"]), gmap["q2_unowed"], flat(gmap["q3"]), flat(gmap["q4b"]), flat(gmap["q4c"]), gmap["q4d"]]


def observations(run: Path, slot: dict, rec: dict, gmap: dict, disp: dict, dev: bool, route: bool) -> tuple[list, list, set]:
    items, obs, unresolved, used = items_of(run), [], [], set()

    def v(k):
        m = items[k]
        o = m.get("oracle")
        r = None
        if o and o.get("mode") == "binding" and o.get("verdict") in SCORABLE:
            r = o["verdict"]
        elif disp.get(f"{rec['name']}::{k}") in SCORABLE:
            r = disp[f"{rec['name']}::{k}"]
        elif dev and o and o.get("verdict") in SCORABLE:
            r = o["verdict"]
        if r is None and not (o and o.get("verdict") == "not-applicable"):
            unresolved.append(k)
        return r

    if route and not slot.get("scored"):
        return obs, unresolved, None
    specs = mapped_specs(gmap)
    for k, m in items.items():
        if any(matches(k, m, sp) for sp in specs) or m.get("critical"):
            used.add(m["measure"])
    arm, owed, non_owed = slot["arm"], 0, bool(slot.get("non_owed"))
    if arm == "cand":
        req = [(k, v(k)) for k, m in items.items() if m["measure"] in gmap["q2_owed"] and not matches(k, m, gmap["q2_unowed"])]
        if req:
            owed = len(req)
            unowed = sum(v(k) == "fail" for k, m in items.items() if matches(k, m, gmap["q2_unowed"]))
            obs.append({"g": "Q2", "owed": owed, "met": sum(r == "pass" for _, r in req), "unowed": unowed})
    if arm in ("cand", "b1"):
        for k, m in items.items():
            fam = gmap["q3"].get(m["measure"])
            if fam and (r := v(k)) is not None:
                obs.append({"g": "Q3", "fam": fam, "score": SCORABLE[r], "item": k})
    for k, m in items.items():
        if m.get("critical") and (r := v(k)) is not None:
            obs.append({"g": "Q4a", "err": 1 - SCORABLE[r], "item": k})
    if slot.get("scored", True):
        for gate, key in (("Q4b", "q4b"), ("Q4c", "q4c")):
            rs = [v(k) for k, m in items.items() if m["measure"] in gmap[key]]
            obs.append({"g": gate, "hit": int("fail" in rs)})
        if non_owed:
            rs = [v(k) for k, m in items.items() if matches(k, m, gmap["q4d"])]
            obs.append({"g": "Q4d", "hit": int("fail" in rs)})
    return obs, sorted(set(unresolved)), used


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--declaration", type=Path, required=True)
    ap.add_argument("--map", type=Path, required=True)
    ap.add_argument("--runs", type=Path, action="append", required=True)
    ap.add_argument("--rerun", type=Path, action="append", default=[])
    ap.add_argument("--dispositions", type=Path)
    ap.add_argument("--dev-advisory-as-evaluator", action="store_true")
    ap.add_argument("--subject-commit", action="append", default=[], metavar="ARMKEY=COMMIT")
    ap.add_argument("--allow-unchecked-subject", action="store_true")
    ap.add_argument("--allow-unresolved", action="store_true")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--audit", type=Path)
    a = ap.parse_args()

    decl, gmap = json.loads(a.declaration.read_text()), json.loads(a.map.read_text())
    disp = json.loads(a.dispositions.read_text()) if a.dispositions else {}
    expect = dict(x.split("=", 1) for x in a.subject_commit)
    arms, routes = decl["arms"], decl.get("q5c_routes", [])
    mode, purpose = decl.get("execution_mode", "qualification"), decl.get("purpose", "qualification")
    infra = decl.get("infra_error_patterns", DEFAULT_INFRA)
    findings: list[dict] = []
    bad = lambda what, **kw: findings.append({"kind": "INTEGRITY", "what": what, **kw})  # noqa: E731

    if len(set(arms.values())) != len(arms):
        bad("two arm labels share one run-name arm key", arms=arms)

    def collect(roots):
        out = collections.defaultdict(list)
        for root in roots:
            for d in sorted(root.glob("*/*-r*")) + sorted(root.glob("*-r*")):
                if (d / "summary.json").exists():
                    out[d.name].append(classify(d, infra))
        return out

    orig, rer = collect(a.runs), collect(a.rerun)
    declared = {}
    for slot in decl["slots"]:
        name = f"{slot['episode']}-{arms[slot['arm']]}-r{slot.get('replicate', 0)}"
        if name in declared:
            bad("duplicate slot in declaration", run=name)
        declared[name] = slot
    keys = set(arms.values())
    other = sorted(n for n in set(orig) | set(rer) if n.rsplit("-", 2)[1] not in keys)
    for name in sorted((set(orig) | set(rer)) - set(declared) - set(other)):
        bad("undeclared run", run=name)

    runs, reruns, used_measures, gated_runs = [], [], set(), 0
    profile_keys = collections.Counter()
    for name, slot in declared.items():
        tries, rr = orig.get(name, []), rer.get(name, [])
        if not tries:
            bad("declared slot has no original run", run=name)
            continue
        if len(tries) > 1 or len(rr) > 1:
            bad("more than one original or rerun directory for a slot", run=name, dirs=[t["dir"] for t in tries + rr])
        first, final = tries[0], (rr[0] if rr else tries[0])
        if rr:
            reruns.append({"run": name, "original": first["dir"], "rerun": rr[0]["dir"], "original_kind": first["kind"], "rerun_kind": rr[0]["kind"]})
            if first["kind"] != "infra":
                bad("rerun of a slot whose original was not a provider-transport failure", run=name, original_kind=first["kind"])
        arm_key = arms[slot["arm"]]
        for t in tries + rr:
            s = t["summary"]
            want, have = expect.get(arm_key), s.get("subject_commit")
            if want is None and not a.allow_unchecked_subject:
                bad("no expected subject commit given for the arm", run=name, arm=arm_key)
            elif want and have != want:
                bad("subject commit mismatch", run=name, have=have, want=want)
            if "delivered" not in (s.get("activation") or {}):
                if arm_key not in decl.get("no_activation_arms", []):
                    bad("activation record absent", run=name)
            elif not s["activation"]["delivered"]:
                bad("activation not delivered", run=name)
            if s.get("execution_mode") != mode:
                bad("execution mode differs from the declaration", run=name, have=s.get("execution_mode"), want=mode)
            if (s.get("accounting") or {}).get("purpose") != purpose:
                bad("accounting purpose differs from the declaration", run=name, have=(s.get("accounting") or {}).get("purpose"), want=purpose)
            profile_keys[s.get("profile_key_sha256")] += 1
        admissible = final["kind"] in ("ok", "death")
        rec = {"run": name, "episode": slot["episode"], "arm": slot["arm"], "admissible": admissible, "death": final["kind"] == "death",
               "kind": final["kind"], "identities": [t["dir"] for t in tries + rr], "obs": []}
        if admissible:
            route = slot["episode"].split("-")[0] in routes
            rec["obs"], rec["unresolved_items"], used = observations(Path(final["dir"]), slot, final, gmap, disp, a.dev_advisory_as_evaluator, route)
            if used is not None:
                used_measures |= used
                gated_runs += 1
            if route and slot["arm"] in ("cand", "b65"):
                s, ro = final["summary"], final["summary"].get("resource_observation", {})
                native = s["installed_entrypoint_bytes"] + sum(b for f, b in s["active_ssdp_files"].items()
                                                               if f in ro.get("native_files", []) and not f.endswith("/SKILL.md"))
                rec["obs"].append({"g": "Q5c", "route": slot["episode"].split("-")[0], "bytes": s["active_ssdp_bytes"],
                                   "native_bytes": native, "mode": s["ssdp_read_mode"]})
            if any(o["g"] == "Q2" for o in rec["obs"]) and slot.get("non_owed"):
                bad("run is declared non-owed but carries owed delegate requests", run=name)
            if rec["unresolved_items"] and not a.allow_unresolved:
                findings.append({"kind": "UNRESOLVED", "what": "mapped items without a resolved verdict", "run": name, "items": rec["unresolved_items"]})
        runs.append(rec)

    for label, spec in zip(("q2_owed", "q2_unowed", "q3", "q4b", "q4c", "q4d"), mapped_specs(gmap)):
        missing = [m for m in spec.get("measures", []) if m not in used_measures]
        if missing and gated_runs:
            bad("mapped measure matches no item in any built run", gate=label, measures=missing)
    want_profile = decl.get("profile_key_sha256")
    if want_profile:
        if set(profile_keys) - {want_profile}:
            bad("runs with a profile key other than the declared one", seen=dict(profile_keys))
    elif not decl.get("unchecked_profile"):
        bad("no profile key declared")

    pair = {"checked": False}
    if decl.get("check_pair_order", True):
        by_ep = collections.defaultdict(dict)
        for rec in runs:
            if rec["arm"] in ("cand", "b1"):
                t = orig[rec["run"]][0]
                by_ep[rec["episode"]][rec["arm"]] = t["summary"].get("pair_order")
        first = collections.Counter()
        for ep, po in by_ep.items():
            if set(po) != {"cand", "b1"}:
                continue
            if po["cand"] != po["b1"] or sorted(po["cand"] or []) != sorted([arms["cand"], arms["b1"], *([arms["b2"]] if "b2" in arms else [])]):
                bad("pair_order missing or inconsistent between the candidate and B1 runs", episode=ep, pair_order=po)
                continue
            order = [x for x in po["cand"] if x in (arms["cand"], arms["b1"])]
            first[order[0]] += 1
        pair = {"checked": True, "first_arm": dict(first)}
        if first and abs(first[arms["cand"]] - first[arms["b1"]]) > 1:
            bad("order is not alternating", first_arm=dict(first))

    record = {"runs": runs, "reruns": reruns,
              "descriptive": {"builder": "build_campaign_record.py", "development_advisory_included": bool(a.dev_advisory_as_evaluator),
                              "dispositions": a.dispositions.name if a.dispositions else None,
                              "unresolved_items": sum(len(r.get("unresolved_items", [])) for r in runs), "pair_order": pair}}
    audit = {"declared": len(declared), "built": len(runs), "reruns": len(reruns), "ignored_other_arms": len(other), "pair_order": pair,
             "by_arm": {k: dict(collections.Counter("admissible" if r["admissible"] else "inadmissible" for r in runs if r["arm"] == k))
                        for k in sorted({r["arm"] for r in runs})},
             "findings": findings}
    if a.out:
        a.out.write_text(json.dumps(record, indent=1) + "\n")
    if a.audit:
        a.audit.write_text(json.dumps(audit, indent=1) + "\n")
    print(json.dumps(audit, indent=1))
    if any(f["kind"] == "INTEGRITY" for f in findings):
        sys.exit(3)
    sys.exit(4 if findings else 0)


if __name__ == "__main__":
    main()
