#!/usr/bin/env python3
"""Precondition C(b) runner: the frozen evaluator judges the custodian's 40 calibration items; the custodian's score_cb.py scores them.

  campaign_cb.py run --work WORK --view-dir DIR --rubric FILE [--task-doc FILE] --out cb-results.json [--limit N] [--parallel N]
      One evaluator session per item, in OMP containment with the frozen evaluator profile (the same launch path as assess70.py).
      The bundle holds only: the item's evaluator-view file (under item.json), the rubric (shared-rubric.txt) and the task text.
      No labels, no episode keys. Needs SSDP70_OMP_PROVIDER_CREDENTIAL. It writes {"<neutral id>": {"result", "evidence"}} and the
      raw evaluator traces next to --out (cb-traces/<id>.jsonl). Items it could not parse are written as {"result": "invalid"}.
  campaign_cb.py cost --work WORK --traces DIR --price-in P --price-cached P --price-out P

The runner never reads labels. Scoring is `python3 <store>/operator/score_cb.py cb-results.json`, which prints counts only.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVAL = HERE.parents[0] / "eval"
sys.path.insert(0, str(EVAL))
import assess70  # noqa: E402
import core70  # noqa: E402

TASK = """You are an independent evaluator. You did not write the report you are judging and must not trust it.

Read task.md (this file), task-details.md (if present), shared-rubric.txt (the frozen rubric) and item.json (one calibration item; its "id" is the id to return). Apply the rubric section that
matches the item's gate to the item and nothing else. Do not use the network, shell, skills or agents. If the evidence in item.json does
not decide the question, answer "unresolved"; never guess a pass. Generic or boilerplate text never earns a pass where the rubric
requires case-specific content.

Return strict JSON only, no other text:
{"item": "<the id given in item.json>", "result": "pass|fail|unresolved", "evidence": "<=40 words"}
"""


def parse(text: str | None, item_id: str) -> dict:
    if not text:
        return {"result": "invalid", "evidence": "no result text"}
    try:
        o = json.loads(text[text.index("{"):text.rindex("}") + 1])
    except ValueError:
        return {"result": "invalid", "evidence": "unparseable"}
    ok = isinstance(o, dict) and o.get("item") == item_id and o.get("result") in ("pass", "fail", "unresolved") and isinstance(o.get("evidence", ""), str)
    return {"result": o["result"], "evidence": " ".join(str(o.get("evidence", "")).split()[:40])} if ok else {"result": "invalid", "evidence": "wrong shape or id"}


def build_bundle(item_file: Path, rubric: Path, root: Path, task_doc: Path | None = None) -> str:
    item = {"id": item_file.stem, **json.loads(item_file.read_text())}      # the neutral id is the file name; the item itself carries no label
    (root / ".qualification-tmp").mkdir(parents=True, exist_ok=True)
    (root / "item.json").write_text(json.dumps(item, indent=1, sort_keys=True))
    if task_doc is not None:
        (root / "task-details.md").write_text(assess70.redact(task_doc.read_text(encoding="utf-8")), encoding="utf-8")
    (root / "shared-rubric.txt").write_text(assess70.redact(rubric.read_text(encoding="utf-8")), encoding="utf-8")
    (root / "task.md").write_text(TASK)
    (root / "EVIDENCE-MANIFEST.json").write_text(json.dumps({"schema": 1, "files": sorted(p.name for p in root.iterdir() if p.is_file())}))
    return item_file.stem


def evaluate(item_file: Path, a, adapter, evaluator) -> tuple[str, dict, str]:
    with tempfile.TemporaryDirectory(prefix="ssdp70-cb-") as tmp:
        bundle, home = Path(tmp) / "bundle", Path(tmp) / "evaluator-private" / "runtime-home"
        bundle.mkdir()
        home.mkdir(parents=True)
        item_id = build_bundle(item_file, a.rubric, bundle, getattr(a, "task_doc", None))
        env = adapter.clean_env()
        env.update({"HOME": str(home), "XDG_CONFIG_HOME": str(home / ".config"), "XDG_CACHE_HOME": str(home / ".cache"),
                    "TMPDIR": str(bundle / ".qualification-tmp"), "TMP": str(bundle / ".qualification-tmp"), "TEMP": str(bundle / ".qualification-tmp")})
        adapter.realize_containment(evaluator.profile, bundle, env)
        launched = adapter.launch(evaluator.profile, TASK, bundle, env)
        text, final = assess70.result_text(launched["stdout"])
    result = parse(text, item_file.stem)
    if launched["returncode"] != 0 or (final or {}).get("is_error"):
        result = {"result": "invalid", "evidence": f"evaluator process failed (returncode {launched['returncode']})"}
    return item_file.stem, result, launched["stdout"]


def cmd_run(a, adapter=None) -> int:
    if not os.environ.get("SSDP70_OMP_PROVIDER_CREDENTIAL") and adapter is None:
        print("SSDP70_OMP_PROVIDER_CREDENTIAL is not set", file=sys.stderr)
        return 2
    keys = a.work / "keys"
    evaluator = core70.load_profile(keys / "omp-evaluator-readonly.json", keys / "omp-evaluator-readonly.capabilities.json")
    errors = core70.profile_claim_errors(evaluator, [])
    if errors:
        print("evaluator profile refused:", errors, file=sys.stderr)
        return 2
    adapter = adapter or assess70.load_adapter("omp_eval")
    files = sorted(Path(a.view_dir).glob("cb-*.json"))
    if a.limit:
        files = files[:a.limit]
    if not files:
        print("no cb-*.json items in the view directory", file=sys.stderr)
        return 2
    traces = a.out.parent / "cb-traces"
    traces.mkdir(parents=True, exist_ok=True)
    results = {}
    with cf.ThreadPoolExecutor(max_workers=a.parallel) as pool:
        for name, res, raw in pool.map(lambda f: evaluate(f, a, adapter, evaluator), files):
            results[name] = res
            (traces / f"{name}.jsonl").write_text(raw)
    a.out.write_text(json.dumps(results, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"items": len(results), "invalid": sum(r["result"] == "invalid" for r in results.values()), "out": str(a.out)}))
    return 0


def cmd_cost(a) -> int:
    sys.path.insert(0, str(HERE))
    import campaign_assess
    files = sorted(Path(a.traces).glob("*.jsonl"))
    if not files:
        print("no traces")
        return 2
    rows = [campaign_assess.trace_usage(f) for f in files]
    t = {k: sum(r[k] for r in rows) for k in rows[0]}
    usd = (t["input"] * a.price_in + t["cacheRead"] * a.price_cached + t["output"] * a.price_out) / 1e6
    print(json.dumps({"items": len(rows), "mean_turns": round(t["turns"] / len(rows), 1), "cache_hit_rate": round(t["cacheRead"] / max(1, t["cacheRead"] + t["input"]), 3),
                      "total_usd": round(usd, 4), "mean_usd_per_item": round(usd / len(rows), 5)}, indent=1))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--work", type=Path, required=True)
    r.add_argument("--view-dir", type=Path, required=True)
    r.add_argument("--rubric", type=Path, required=True)
    r.add_argument("--task-doc", type=Path, help="the custodian's EVALUATOR-TASK.md (copied into the bundle as task-details.md)")
    r.add_argument("--out", type=Path, required=True)
    r.add_argument("--limit", type=int)
    r.add_argument("--parallel", type=int, default=4)
    k = sub.add_parser("cost")
    k.add_argument("--work", type=Path, required=True)
    k.add_argument("--traces", type=Path, required=True)
    for f in ("price-in", "price-cached", "price-out"):
        k.add_argument(f"--{f}", type=float, required=True)
    a = ap.parse_args()
    return cmd_run(a) if a.cmd == "run" else cmd_cost(a)


if __name__ == "__main__":
    raise SystemExit(main())
