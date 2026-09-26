"""Apply the frozen R0/R2 rules (scenarios.yaml `rework`) to results/rework/live-r1r2 (evidence tooling only).

Usage: python rework_gates.py assess|evaluate
"""
import gzip
import json
import re
import statistics
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

EVAL = Path(__file__).resolve().parent
OUT = EVAL / "results/rework/live-r1r2"
sys.path.insert(0, str(EVAL))
import harness  # noqa: E402
import yaml  # noqa: E402

RUBRICS = yaml.safe_load((EVAL / "rubrics.yaml").read_text())
SCEN = {s["id"]: s for split in yaml.safe_load((EVAL / "scenarios.yaml").read_text())["trajectories"].values() for s in split}


def runs():
    for d in sorted(OUT.iterdir()):
        if (d / "summary.json").is_file():
            scenario, variant, rep = d.name.rsplit("-", 2)
            yield d, scenario, variant, rep


def assess_all():
    todo = [(d, s) for d, s, _, _ in runs() if not (d / "assessment.json").is_file()]

    def one(item):
        d, s = item
        v = harness.assess(d, EVAL / "fixtures" / SCEN[s]["fixture"], RUBRICS[s], "claude-opus-5-5")
        return d.name, v.get("verdict")

    with ThreadPoolExecutor(4) as pool:
        for name, verdict in pool.map(one, todo):
            print(name, verdict, flush=True)


def isolation(d):
    gz = d / "trace.jsonl.gz"
    raw = gzip.decompress(gz.read_bytes()).decode() if gz.is_file() else ((d / "trace.jsonl").read_text() if (d / "trace.jsonl").is_file() else "")
    init = next((json.loads(line) for line in raw.splitlines() if '"subtype":"init"' in line.replace(" ", "")), {})
    names = [s if isinstance(s, str) else s.get("name") for s in init.get("skills") or []]
    ssdp = [n for n in names if n in harness.SSDP_SKILLS]
    bases = set(re.findall(r"Base directory for this skill: (\S+?)(?:\\n|\s)", raw))
    return {"ssdp_once": sorted(ssdp) == sorted(harness.SSDP_SKILLS), "bases_project": all("/project/.claude/skills/" in b for b in bases),
            "bases": len(bases), "cc": init.get("claude_code_version"), "model": init.get("model")}


def evaluate():
    rows = {}
    for d, s, v, rep in runs():
        summ = json.loads((d / "summary.json").read_text())
        eb = summ["entry_and_burden"]
        a = json.loads((d / "assessment.json").read_text()).get("verdict") if (d / "assessment.json").is_file() else None
        rows[d.name] = {"scenario": s, "variant": v, "rep": rep, "assessment": a, "is_error": summ.get("is_error"),
                        "oracle": summ.get("oracle"), "isolation": isolation(d), "num_turns": summ.get("num_turns"),
                        "cost_usd": summ.get("total_cost_usd"), "input_tokens": summ.get("input_tokens_total"),
                        **{k: eb[k] for k in ("governing_stated_before_protocol_action_or_mutation", "governing_stated_before_mutation",
                                              "governing_knowable_index", "first_protocol_action_index", "first_mutation_index",
                                              "governing_stated_index", "remote_or_source_lookups", "versioning_owner_reads",
                                              "observed_active_ssdp_bytes", "ssdp_entrypoint_bytes", "ssdp_reference_read_bytes",
                                              "protocol_file_reads")}}
    sel = lambda s, v: [r for r in rows.values() if r["scenario"].startswith(s) and r["variant"] == v]  # noqa: E731
    gates = {}
    r1 = {}
    for s in ("T6", "T5", "T4"):
        cand = sel(s, "v66")
        r1[s] = {"runs": len(cand), "pass": sum(1 for r in cand if r["governing_stated_before_protocol_action_or_mutation"] and r["assessment"] == "PASS"),
                 "baseline_pass": sum(1 for r in sel(s, "v65") if r["governing_stated_before_protocol_action_or_mutation"] and r["assessment"] == "PASS"),
                 "baseline_runs": len(sel(s, "v65"))}
    gates["R1_version"] = r1
    gates["R1_T6_zero_silent_mismatch"] = r1["T6"]["runs"] == 4 and r1["T6"]["pass"] == 4
    gates["R1_all_version_cases"] = all(v["pass"] == v["runs"] and v["runs"] > 0 for v in r1.values())
    nl = [r for s in ("T1", "T7") for r in sel(s, "v66")]
    gates["no_lookup_unversioned"] = {"runs": len(nl), "violations": [r for r in nl if r["remote_or_source_lookups"] or r["versioning_owner_reads"]]}
    burden = {}
    for s in ("T1", "T7"):
        a, b = [r["observed_active_ssdp_bytes"] for r in sel(s, "v65")], [r["observed_active_ssdp_bytes"] for r in sel(s, "v66")]
        pa, pb = [r["protocol_file_reads"] for r in sel(s, "v65")], [r["protocol_file_reads"] for r in sel(s, "v66")]
        ok = bool(a and b) and statistics.median(b) <= 0.85 * statistics.median(a) and max(b) < min(a)
        burden[s] = {"v65_bytes": a, "v66_bytes": b, "v65_median": a and statistics.median(a), "v66_median": b and statistics.median(b),
                     "v65_reads": pa, "v66_reads": pb, "pass_rule": ok}
    gates["burden"] = burden
    gates["criterion4_live"] = any(v["pass_rule"] for v in burden.values())
    corr = {}
    for s in ("T1", "T2", "T3", "T7"):
        corr[s] = {v: [r["assessment"] for r in sel(s, v)] for v in ("v65", "v66")}
    gates["correctness"] = corr
    gates["isolation_all"] = all(r["isolation"]["ssdp_once"] and r["isolation"]["bases_project"] and r["isolation"]["bases"] >= 1 for r in rows.values())
    gates["errors"] = [k for k, r in rows.items() if r["is_error"]]
    (OUT.parent / "live-r1r2-summary.json").write_text(json.dumps({"gates": gates, "runs": rows}, indent=1, sort_keys=True) + "\n")
    print(json.dumps(gates, indent=1, sort_keys=True, default=str))


if __name__ == "__main__":
    assess_all() if sys.argv[1] == "assess" else evaluate()
