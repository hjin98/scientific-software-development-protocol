#!/usr/bin/env python3
"""Campaign-record builder: run directories -> the `h4.py score` input, with a slot audit.

Workplan 7X S4 follow-up (campaign work order gap 4 and, for the declared slots, gap 2). Analyst tool; it changes no gate,
threshold or margin and reads only run directories, a slot declaration and a gate map. It never opens custody stores,
keys or oracle sources: it reads `summary.json`, `requirements-snapshot.json` (item id, measure, critical),
`oracle-output/*.stdout.txt` (item verdicts) and `events.normalized.jsonl` (termination) from each run.

Declaration (JSON):  {"slots": [{"episode": "EP-001", "arm": "cand", "replicate": 0}, ...],
                      "arms": {"cand": "p72", "b1": "p66", "b2": "p66b", "b65": "p65"},   # h4 label -> run-name arm key
                      "q5c_routes": ["T1", "T7", "T8"]}
Gate map (JSON, optional; defaults below are the development map used for the S4 report):
  {"q2_owed": ["delegate_request"], "q2_unowed_id": "UNOWED.", "q2_unowed_measures": ["unnecessary_probe"],
   "q3": {"measure": "family", ...}, "q4b": [...measures], "q4c": [...], "q4d": [...]}
Observations: Q4b and Q4c are one per admissible run; Q4d is one per admissible run with no owed delegate request
(a builder definition for the checker to confirm against the contract); Q2U carries unowed requests (see h4.q2).
Verdicts: a binding oracle verdict decides. An advisory verdict is unadjudicated and is NOT used, unless a disposition for
(run, item) is supplied with --dispositions (evaluator output: {"<run>::<item>": "pass"|"fail"}). `--dev-advisory-as-evaluator`
treats advisory verdicts as dispositions for development cross-checks only and labels the record so.

Admissibility (contract section 3): COMPLETE_ADMISSIBLE is admissible; EXECUTION_ERROR whose termination is turn_cap or
timeout is behaviour (admissible, death); any other state is infrastructure. An infrastructure slot may be rerun once: pass the
rerun directory after the original; both identities are kept, and a second failure is inadmissible. A rerun of a slot whose
original was not infrastructure is an INTEGRITY finding.

Usage: build_campaign_record.py --declaration D.json --runs DIR [--runs DIR ...] [--map M.json] [--dispositions F.json]
                               [--out CAMPAIGN.json] [--audit AUDIT.json]
Exit 0 clean; 3 when the audit has an INTEGRITY finding (missing, duplicate, undeclared, subject mismatch, rerun misuse).
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

DEFAULT_MAP = {
    "q2_owed": ["delegate_request"],
    "q2_unowed_id": "UNOWED.",
    "q2_unowed_measures": ["unnecessary_probe"],
    "q3": {"detection.named": "finding", "detection.unnamed": "finding", "null_coverage": "null", "variant_disclosure": "variants",
           "tension_report": "tension", "decision_provenance": "choices", "delegated_finding_loss": "delegated",
           "o1_authoring": "o1", "o1_review": "o1"},
    "q4b": ["claim_integrity"],
    "q4c": ["unauthorized_mutation"],
    "q4d": ["over_qualification", "unnecessary_probe"],
}
SCORABLE = {"pass": 1, "fail": 0}


def termination(run: Path) -> str | None:
    p = run / "events.normalized.jsonl"
    if not p.exists():
        return None
    for line in p.read_text().splitlines():
        event = json.loads(line)
        if event.get("kind") == "termination":
            return event["payload"].get("state")
    return None


def classify(run: Path) -> dict:
    s = json.loads((run / "summary.json").read_text())
    state, term = s["evidence_state"], termination(run)
    if state == "COMPLETE_ADMISSIBLE":
        kind = "ok"
    elif state == "EXECUTION_ERROR" and term in ("turn_cap", "timeout"):
        kind = "death"
    elif state == "EXECUTION_ERROR":
        kind = "infra"
    else:
        kind = "malformed"
    return {"summary": s, "state": state, "term": term, "kind": kind, "dir": str(run), "name": run.name}


def items_of(run: Path) -> dict:
    manifest = {i["id"].split("::", 1)[-1]: i for i in json.loads((run / "requirements-snapshot.json").read_text())["expected_scoring_items"]}
    verdicts = {}
    for f in sorted((run / "oracle-output").glob("*.stdout.txt")):
        text = f.read_text().strip()
        if not text:                                       # a route run's oracle may print nothing: its items stay unresolved
            continue
        for key, value in json.loads(text).get("items", {}).items():
            verdicts[key.split("::", 1)[-1]] = value
    return {k: dict(m, oracle=verdicts.get(k)) for k, m in manifest.items()}


def verdict(run_name: str, item: str, entry: dict, dispositions: dict, dev_advisory: bool) -> str | None:
    v = entry.get("oracle")
    d = dispositions.get(f"{run_name}::{item}")
    if v and v.get("mode") == "binding" and v.get("verdict") in SCORABLE:
        return v["verdict"]
    if d in SCORABLE:
        return d
    if dev_advisory and v and v.get("verdict") in SCORABLE:
        return v["verdict"]
    return None


def observations(run: Path, arm: str, rec: dict, gmap: dict, dispositions: dict, dev_advisory: bool, routes: list, ep: str) -> tuple[list, dict]:
    items, obs, unresolved = items_of(run), [], collections.Counter()

    def v(k):
        r = verdict(rec["name"], k, items[k], dispositions, dev_advisory)
        if r is None and items[k].get("oracle") is not None and items[k]["oracle"].get("verdict") in SCORABLE:
            unresolved["advisory-unadjudicated"] += 1
        return r

    owed_run = False
    if arm == "cand":
        req = [(k, v(k)) for k, m in items.items() if m["measure"] in gmap["q2_owed"] and not k.startswith(gmap["q2_unowed_id"])]
        req = [(k, r) for k, r in req if r]
        owed_run = bool(req)
        if req:
            obs.append({"g": "Q2", "owed": len(req), "met": sum(r == "pass" for _, r in req)})
        unowed = sum(v(k) == "fail" for k, m in items.items() if k.startswith(gmap["q2_unowed_id"]) and m["measure"] in gmap["q2_unowed_measures"])
        if unowed or not req:
            obs.append({"g": "Q2U", "unowed": unowed})      # an unowed request arises where none was owed, so it is its own observation
    if arm in ("cand", "b1"):
        for k, m in items.items():
            fam = gmap["q3"].get(m["measure"])
            if fam and (r := v(k)):
                obs.append({"g": "Q3", "fam": fam, "score": SCORABLE[r], "item": k})
    for k, m in items.items():
        if m.get("critical") and (r := v(k)):
            obs.append({"g": "Q4a", "err": 1 - SCORABLE[r], "item": k})
    for gate, key in (("Q4b", "q4b"), ("Q4c", "q4c"), ("Q4d", "q4d")):
        if gate == "Q4d" and owed_run:
            continue                                       # Q4d: one observation per non-owed run (contract section 5)
        rs = [r for k, m in items.items() if m["measure"] in gmap[key] and (r := v(k))]
        obs.append({"g": gate, "hit": int("fail" in rs)})  # a scored run with no failing item is a 0, not an absence
    route = ep.split("-")[0]
    if route in routes and arm in ("cand", "b65"):
        s = rec["summary"]
        ro = s.get("resource_observation", {})
        native = s["installed_entrypoint_bytes"] + sum(b for f, b in s["active_ssdp_files"].items()
                                                       if f in ro.get("native_files", []) and not f.endswith("/SKILL.md"))
        obs.append({"g": "Q5c", "route": route, "bytes": s["active_ssdp_bytes"], "native_bytes": native, "mode": s["ssdp_read_mode"]})
    return obs, dict(unresolved)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--declaration", type=Path, required=True)
    ap.add_argument("--runs", type=Path, action="append", required=True, help="run directory root; give a rerun root after the original")
    ap.add_argument("--map", type=Path)
    ap.add_argument("--dispositions", type=Path)
    ap.add_argument("--dev-advisory-as-evaluator", action="store_true")
    ap.add_argument("--subject-commit", action="append", default=[], metavar="ARM=COMMIT", help="expected subject commit per run-name arm")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--audit", type=Path)
    a = ap.parse_args()

    decl = json.loads(a.declaration.read_text())
    gmap = dict(DEFAULT_MAP, **(json.loads(a.map.read_text()) if a.map else {}))
    disp = json.loads(a.dispositions.read_text()) if a.dispositions else {}
    expect = dict(x.split("=", 1) for x in a.subject_commit)
    arms, routes = decl["arms"], decl.get("q5c_routes", [])

    found: dict[str, list[dict]] = collections.defaultdict(list)    # run name -> [original, rerun...] in --runs order
    for root in a.runs:
        for d in sorted(root.glob("*/*-r*")) + sorted(root.glob("*-r*")):
            if (d / "summary.json").exists():
                found[d.name].append(classify(d))
    declared = {}
    for slot in decl["slots"]:
        name = f"{slot['episode']}-{arms[slot['arm']]}-r{slot.get('replicate', 0)}"
        declared[name] = slot

    findings: list[dict] = []
    keys = set(arms.values())
    other = sorted(n for n in found if n.rsplit("-", 2)[1] not in keys)       # arms outside the declaration: reported, not built
    for name in sorted(n for n in set(found) - set(declared) if n not in other):
        findings.append({"kind": "INTEGRITY", "what": "undeclared run", "run": name})
    seen = collections.Counter(f"{s['episode']}/{s['arm']}/{s.get('replicate', 0)}" for s in decl["slots"])
    findings += [{"kind": "INTEGRITY", "what": "duplicate slot in declaration", "slot": k} for k, n in seen.items() if n > 1]

    runs, reruns = [], []
    for name, slot in declared.items():
        tries = found.get(name, [])
        if not tries:
            findings.append({"kind": "INTEGRITY", "what": "declared slot has no run", "run": name})
            continue
        if len({t["dir"] for t in tries}) != len(tries) or len(tries) > 2:
            findings.append({"kind": "INTEGRITY", "what": "more than one rerun or duplicate directory", "run": name, "dirs": [t["dir"] for t in tries]})
        first, final = tries[0], tries[-1]
        if len(tries) == 2:
            reruns.append({"run": name, "original": first["dir"], "rerun": final["dir"], "original_kind": first["kind"], "rerun_kind": final["kind"]})
            if first["kind"] != "infra":
                findings.append({"kind": "INTEGRITY", "what": "rerun of a slot whose original was not an infrastructure failure", "run": name})
        for t in tries:
            arm_key = arms[slot["arm"]]
            want = expect.get(arm_key)
            have = t["summary"].get("subject_commit")
            if want and have and have != want:
                findings.append({"kind": "INTEGRITY", "what": "subject commit mismatch", "run": name, "have": have, "want": want})
            if not t["summary"].get("activation", {}).get("delivered", True) and arm_key not in ("p66", "p66b"):
                findings.append({"kind": "INTEGRITY", "what": "activation not delivered", "run": name})
        admissible = final["kind"] in ("ok", "death")
        rec = {"run": name, "episode": slot["episode"], "arm": slot["arm"], "admissible": admissible,
               "death": final["kind"] == "death", "identities": [t["dir"] for t in tries], "obs": []}
        if admissible:
            rec["obs"], unresolved = observations(Path(final["dir"]), slot["arm"], final, gmap, disp, a.dev_advisory_as_evaluator, routes, slot["episode"])
            rec["unresolved"] = unresolved
        runs.append(rec)

    record = {"runs": runs, "reruns": reruns,
              "descriptive": {"builder": "build_campaign_record.py",
                              "development_advisory_included": bool(a.dev_advisory_as_evaluator),
                              "dispositions": a.dispositions.name if a.dispositions else None,
                              "unresolved_advisory_items": sum(r.get("unresolved", {}).get("advisory-unadjudicated", 0) for r in runs)}}
    audit = {"declared": len(declared), "found": len(found) - len(other), "built": len(runs), "reruns": len(reruns), "ignored_other_arms": len(other),
             "by_arm": {k: dict(collections.Counter("admissible" if r["admissible"] else "inadmissible" for r in runs if r["arm"] == k))
                        for k in sorted({r["arm"] for r in runs})},
             "findings": findings}
    if a.out:
        a.out.write_text(json.dumps(record, indent=1) + "\n")
    if a.audit:
        a.audit.write_text(json.dumps(audit, indent=1) + "\n")
    print(json.dumps(audit, indent=1))
    sys.exit(3 if any(f["kind"] == "INTEGRITY" for f in findings) else 0)


if __name__ == "__main__":
    main()
