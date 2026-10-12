#!/usr/bin/env python3
"""Reproduce the figures of PROTOCOL-7.1-DEV-PROBE-2026-10-07-RESULT.md.

Read-only over the retained Phase D run artifacts (summary, normalized events, native trace,
package-access ledger and oracle stdout). Opens no custodian key, authoring or per-episode oracle source.
Usage: diagnose_dev_probe_20261007.py [--runs DIR] [--json OUT]
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

DEFAULT_RUNS = Path.home() / "ssdp70-omp-stagef/qualification/requal71-20261006/dev/runs"
OWNER = "scientific-inspectability-and-initiative.md"
# Pre-registered measures (DEV-PROBE-WORK-ORDER.md) -> binding oracle item families.
MEASURES = {"G1": "REQ.", "G2": "R2.HIT.", "G3": "R2.FALSE", "G4-UM": "UM", "G4-O3": "O3."}
OWNER_MENTION = re.compile(r"inspectab|clause below suffices", re.I)


def in_family(item: str, prefix: str) -> bool:
    return item.startswith(prefix) if prefix.endswith(".") else item == prefix


def run_row(d: Path) -> dict:
    summ = json.loads((d / "summary.json").read_text())
    term = {}
    for line in (d / "events.normalized.jsonl").read_text().splitlines():
        e = json.loads(line)
        if e["kind"] == "termination":
            term = e["payload"]
    items = {}
    for f in (d / "oracle-output").glob("*.stdout.txt"):
        for k, v in json.loads(f.read_text()).get("items", {}).items():
            items[k.split("::", 1)[1]] = v
    ledger = json.loads((d / "adapter-artifacts/package-access-ledger.json").read_text())
    owner_ledger = any(OWNER in (e.get("rel") or "") for e in ledger.get("events", []))
    mentions = 0
    for line in (d / "trace.jsonl").read_text().splitlines():
        if line.startswith('{"type":"message_end"'):
            msg = json.loads(line)["message"]
            if msg.get("role") == "assistant":
                mentions += sum(bool(OWNER_MENTION.search(c.get("thinking") or c.get("text") or ""))
                                for c in msg.get("content", []))
    ep, arm, _ = d.name.rsplit("-", 2)
    return {"run": d.name, "ep": ep, "arm": arm, "key": d.parent.name, "state": summ["evidence_state"],
            "activation": summ["criteria"].get("deterministic activation"), "term": term.get("state"),
            "error": (term.get("native_return_state") or {}).get("errorMessage"),
            "owner_seqs": summ.get("owner_read_sequences"), "owner_ledger": owner_ledger,
            "owner_mentions": mentions, "items": items}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=Path, default=DEFAULT_RUNS)
    ap.add_argument("--json", type=Path)
    a = ap.parse_args()
    rows = [run_row(d) for d in sorted(a.runs.glob("*/*-r0"))]
    C = collections.Counter
    out: dict = {"runs": len(rows), "by_key": C(r["key"] for r in rows)}
    out["delivery"] = C(f"{r['arm']}/{r['activation']}" for r in rows)
    out["termination"] = C(f"{r['arm']}/{r['term']}/{r['state']}" for r in rows)
    for arm in ("p71", "p66"):
        n = sum(r["arm"] == arm for r in rows)
        deaths = sum(r["arm"] == arm and r["term"] in ("turn_cap", "timeout") for r in rows)
        out[f"budget_{arm}"] = {"deaths": deaths, "runs": n, "rate": round(deaths / n, 4), "holds": deaths <= 0.05 * n}
    out["provider_errors"] = [(r["run"], r["error"]) for r in rows if r["term"] == "error"]
    for name, prefix in MEASURES.items():
        for arm in ("p71", "p66"):
            v_all, v_adm = C(), C()
            for r in rows:
                if r["arm"] != arm:
                    continue
                for item, v in r["items"].items():
                    if v["mode"] == "binding" and in_family(item, prefix):
                        v_all[v["verdict"]] += 1
                        if r["state"] == "COMPLETE_ADMISSIBLE":
                            v_adm[v["verdict"]] += 1
            out[f"{name}_{arm}"] = {"all": v_all, "admissible": v_adm}
    p71 = [r for r in rows if r["arm"] == "p71"]
    out["G3_failures"] = [(r["run"], r["items"]["R2.FALSE"]["evidence"]) for r in p71
                          if r["items"].get("R2.FALSE", {}).get("verdict") == "fail"]
    out["G1_failures"] = [(r["run"], i, v["evidence"]) for r in p71 for i, v in r["items"].items()
                          if i.startswith("REQ.") and v["verdict"] != "pass"]
    # Ledger cross-check of the native-read owner observation, and G2 miss classes.
    agree, g2_miss = C(), []
    for r in p71:
        for i, v in r["items"].items():
            if i.startswith("R2.HIT.") or i == "R2.FALSE":
                agree[f"{i.split('.')[1]}/{v['verdict']}/ledger_owner={r['owner_ledger']}"] += 1
            if i.startswith("R2.HIT.") and v["verdict"] == "fail":
                g2_miss.append((r["run"], i, r["owner_mentions"], r["owner_ledger"], v["evidence"]))
    out["owner_ledger_agreement"] = agree
    out["G2_misses"] = g2_miss
    out["G2_miss_owner_never_mentioned"] = sum(m[2] == 0 for m in g2_miss)
    text = json.dumps(out, indent=1, default=str)
    if a.json:
        a.json.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
