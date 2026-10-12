#!/usr/bin/env python3
"""Bounded-sensitivity analysis of unresolved assessments (stakeholder eleventh ruling, 2026-10-11). Offline; no provider call.

  bounded_sensitivity.py cc    WORK --map M --c-a A --c-b B --static S --assessment-root P [--rerun-root R] --out-dir D
      Stage 1, Precondition C(c) (the A/A screen), blind to the candidate. The unresolved items of B1 and B2 take every combination of
      all-pass / all-fail (four corners) and --random N (default 500) seeded random fillings; the candidate's unresolved items are fixed at pass and are never
      examined (`h4` drops candidate runs for C(c)). Writes D/cc.json. C(c) is established only if it holds at every filling evaluated.
  bounded_sensitivity.py gates WORK ... --out-dir D
      Stage 2, refused unless D/cc.json says established and is current. Scores the gates at W (candidate unresolved items fail, baseline
      unresolved items pass: the worst case for every gate, because pass is the favourable value of every item) and B (the reverse), and at the
      same random fillings as a monotonicity check. Gate classes: ROBUST PASS (passes at W), ROBUST FAIL (fails at B), FRAGILE (passes at B and not
      at W). A random filling outside the bracket [W, B] is reported and voids the monotonicity assumption.

Unresolved items are exactly the items the campaign-record builder cannot resolve from a binding oracle verdict or a VALID assessment. Nothing
here edits a run, an assessment or a gate rule; every output is labelled bounded-sensitivity and is not a complete-data result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import h4  # noqa: E402

SEED = 20261011
LABEL = "BOUNDED-SENSITIVITY (not a complete-data result; stakeholder eleventh ruling)"
ARMS = ("cand", "b1", "b2")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd: list, **kw) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *map(str, cmd)], capture_output=True, text=True, **kw)


def fill(base: dict, unresolved: dict, choose) -> dict:
    """Dispositions = the valid ones plus a value for every unresolved item; choose(arm, key) returns "pass" or "fail"."""
    out = dict(base)
    for arm, keys in unresolved.items():
        for key in keys:
            if key in base:
                raise ValueError(f"{key} is already resolved")
            out[key] = choose(arm, key)
    return out


def corner_fillings():
    """(label, chooser) for the four B1/B2 corners; the candidate is fixed at pass (not examined by C(c))."""
    for b1 in ("pass", "fail"):
        for b2 in ("pass", "fail"):
            yield f"b1-{b1}/b2-{b2}", (lambda arm, key, b1=b1, b2=b2: {"b1": b1, "b2": b2}.get(arm, "pass"))


def random_chooser(seed: int, index: int, arms=ARMS):
    """An independent fair coin for each unresolved item of the given arms, reproducible from (seed, index); other arms pass."""
    def choose(arm, key):
        if arm not in arms:
            return "pass"
        return "pass" if random.Random(f"{seed}:{index}:{key}").random() < 0.5 else "fail"
    return choose


def classify(w: str, b: str) -> str:
    if w == h4.PASS:
        return "ROBUST PASS"
    if b != h4.PASS:
        return "ROBUST FAIL"
    return "FRAGILE"


class Analysis:
    def __init__(self, a):
        self.a = a
        self.scratch = Path(tempfile.mkdtemp(prefix="bounded-sens-"))
        self.base = self.unresolved = None

    def builder_cmd(self, disp: Path, out: Path, allow: bool) -> list:
        w = self.a.work
        arms = json.loads((w / "campaign-identity.json").read_text())["arms"]
        cmd = [HERE / "build_campaign_record.py", "--declaration", w / "declaration.effective.json", "--map", self.a.map, "--dispositions", disp,
               "--out", out]
        for root in sorted((w / "runs").glob("*")):
            if root.is_dir() and not root.name.startswith("rerun"):
                cmd += ["--runs", root]
        for name, row in arms.items():
            cmd += ["--subject-commit", f"{name}={row['commit']}"]
        return cmd + (["--allow-unresolved"] if allow else [])

    def load_base(self):
        """Valid dispositions (collect) and the unresolved items per arm (builder run with the unresolved-waiver, used only to list them)."""
        a = self.a
        base = self.scratch / "base-disp.json"
        cmd = [HERE / "campaign_assess.py", "collect", a.work, "--panels", *a.panels, "--assessment-root", a.assessment_root, "--out", base]
        if a.rerun_root:
            cmd += ["--rerun-root", a.rerun_root]
        run(cmd)                                                     # exit 4 is expected while assessments are unresolved; the file is still written
        self.base = json.loads(base.read_text())
        rec = self.scratch / "base-record.json"
        p = run(self.builder_cmd(base, rec, allow=True))
        if p.returncode != 0:
            sys.exit(f"the base record did not build (exit {p.returncode}): {p.stderr[-300:]}")
        record = json.loads(rec.read_text())
        self.unresolved = {}
        for r in record["runs"]:
            for key in r.get("unresolved_items") or []:
                self.unresolved.setdefault(r["arm"], []).append(f"{r['run']}::{key}")
        extra = set(self.unresolved) - set(ARMS)
        if extra or any(k.startswith("ORPHAN") for ks in self.unresolved.values() for k in ks):
            sys.exit(f"unresolved items outside the candidate and baseline arms or orphan items: {sorted(extra)}")
        self.unresolved = {k: sorted(v) for k, v in self.unresolved.items()}
        return self

    def identity(self) -> dict:
        return {"seed": SEED, "random": self.a.random, "tool_sha256": sha(Path(__file__)), "h4_sha256": sha(HERE / "h4.py"),
                "base_dispositions_sha256": hashlib.sha256(json.dumps(self.base, sort_keys=True).encode()).hexdigest(),
                "unresolved_sha256": hashlib.sha256(json.dumps(self.unresolved, sort_keys=True).encode()).hexdigest(),
                "unresolved_counts": {k: len(v) for k, v in self.unresolved.items()}}

    def record_for(self, choose) -> dict:
        disp = self.scratch / "disp.json"
        disp.write_text(json.dumps(fill(self.base, self.unresolved, choose)))
        rec, final = self.scratch / "record.json", self.scratch / "final.json"
        p = run(self.builder_cmd(disp, rec, allow=False))
        if p.returncode != 0:
            sys.exit(f"a filled record did not build cleanly (exit {p.returncode}): {p.stdout[-300:]} {p.stderr[-300:]}")
        p = run([HERE / "prepare_campaign.py", "assemble", "--work", self.a.work, "--record", rec, "--c-a", self.a.c_a, "--c-b", self.a.c_b,
                 "--static", self.a.static, "--attempt", str(self.a.attempt), "--out", final])
        if p.returncode != 0:
            sys.exit(f"assemble failed: {p.stderr[-300:]}")
        record = json.loads(final.read_text())
        record.setdefault("descriptive", {})["bounded_sensitivity"] = LABEL
        return record


def cc_stage(an: Analysis, out_dir: Path) -> dict:
    results = []
    cases = list(corner_fillings()) + [(f"random-{i}", random_chooser(SEED, i, ("b1", "b2"))) for i in range(an.a.random)]
    for label, choose in cases:
        record = an.record_for(choose)
        record["runs"] = [r for r in record["runs"] if r["arm"] in ("b1", "b2")]          # C(c) is computed blind to candidate results
        pc = h4.precondition_c(h4.Campaign(record))
        results.append({"filling": label, "C(a)": pc["C(a)"], "C(b)": pc["C(b)"], "C(c)": pc["C(c)"], "aa": pc["aa"]})
    established = all(r["C(a)"] and r["C(b)"] and r["C(c)"] for r in results)
    worst = {k: max((r["aa"][k]["diff"] / r["aa"][k]["limit"]) if r["aa"][k]["limit"] else 0 for r in results) for k in results[0]["aa"]}
    out = {"label": LABEL, "identity": an.identity(), "fillings_evaluated": len(results), "established": established,
           "failing_fillings": [r["filling"] for r in results if not (r["C(a)"] and r["C(b)"] and r["C(c)"])],
           "max_diff_over_limit_by_gate": {k: round(v, 3) for k, v in worst.items()}, "corners": results[:4]}
    (out_dir / "cc.json").write_text(json.dumps(out, indent=1) + "\n")
    return out


def gates_stage(an: Analysis, out_dir: Path) -> dict:
    cc_path = out_dir / "cc.json"
    cc = json.loads(cc_path.read_text()) if cc_path.is_file() else {}
    if not cc.get("established") or cc.get("identity") != an.identity():
        print("refused: Precondition C(c) is not established for the current inputs (run `cc` first); candidate gates are not computed")
        return {"refused": True}
    def gates_of(choose):
        res = h4.score(an.record_for(choose))
        return res, {g: v["status"] for g, v in res["gates"].items()} if "gates" in res else {}
    W, wg = gates_of(lambda arm, key: "fail" if arm == "cand" else "pass")
    B, bg = gates_of(lambda arm, key: "pass" if arm == "cand" else "fail")
    if not wg or not bg:
        print("a bracket scoring did not reach the gates (Precondition failed)")
        return {"refused": True}
    seen = {g: set() for g in wg}
    outside = []
    for i in range(an.a.random):
        _, rg = gates_of(random_chooser(SEED, i))
        for g, s in rg.items():
            seen[g].add(s)
            if (wg[g] == h4.PASS and s != h4.PASS) or (bg[g] != h4.PASS and s == h4.PASS):
                outside.append({"filling": i, "gate": g, "status": s})
    table = {g: {"W": wg[g], "B": bg[g], "class": classify(wg[g], bg[g]), "random_statuses": sorted(seen[g])} for g in wg}
    classes = [t["class"] for t in table.values()]
    overall = ("OUTSIDE BRACKET (monotonicity voided)" if outside else "ROBUST FAIL" if "ROBUST FAIL" in classes else
               "FRAGILE: not establishable" if "FRAGILE" in classes else "ROBUST PASS")
    out = {"label": LABEL, "identity": an.identity(), "overall": overall, "gates": table, "outside_bracket": outside[:20],
           "W": {"verdict": W["verdict"], "first_failing_gate": W.get("first_failing_gate"), "gates": W["gates"], "families": W["families"]},
           "B": {"verdict": B["verdict"], "first_failing_gate": B.get("first_failing_gate"), "gates": B["gates"], "families": B["families"]}}
    (out_dir / "gates.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("cc", "gates"))
    ap.add_argument("work", type=Path)
    for name in ("map", "c-a", "c-b", "static", "assessment-root", "out-dir"):
        ap.add_argument(f"--{name}", type=Path, required=True)
    ap.add_argument("--rerun-root", type=Path)
    ap.add_argument("--panels", nargs="+", default=["main", "versioning", "sentinels", "sentinels-add"])
    ap.add_argument("--attempt", type=int, default=2)
    ap.add_argument("--random", type=int, default=500)
    a = ap.parse_args(argv)
    a.out_dir.mkdir(parents=True, exist_ok=True)
    an = Analysis(a).load_base()
    print(json.dumps({"label": LABEL, "unresolved_counts": {k: len(v) for k, v in an.unresolved.items()}}))
    out = cc_stage(an, a.out_dir) if a.stage == "cc" else gates_stage(an, a.out_dir)
    if a.stage == "cc":
        print(json.dumps({k: out[k] for k in ("fillings_evaluated", "established", "failing_fillings", "max_diff_over_limit_by_gate")}, indent=1))
        return 0 if out["established"] else 2
    if out.get("refused"):
        return 2
    print(json.dumps({"overall": out["overall"], "gates": {g: t["class"] for g, t in out["gates"].items()}}, indent=1))
    return 0 if out["overall"] == "ROBUST PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
