#!/usr/bin/env python3
"""P9 driver: run the blinded evaluator (`eval/assess70.py`) over completed campaign runs, and collect its dispositions.

  campaign_assess.py run WORK --keys-root KEYS --evaluator-profile P --evaluator-capabilities C [--shared-rubric R] [--parallel N]
      Every run directory under WORK/runs/<panel>-cNN whose panel is in --panels (default main, versioning, sentinels, sentinels-add: routing, unversioned and burden items are binding or recorded bytes) and whose summary is COMPLETE_ADMISSIBLE and whose arm is an assessed arm (the arms specification WORK/arms-spec.json,
      arms_spec.py; without one p72, p66 or p66b) and that has no assessment.json yet. Needs SSDP70_OMP_PROVIDER_CREDENTIAL. Exits non-zero on the first evaluator failure that is not a
      per-run result (exit codes 0, 1 and 2 of assess70 are results: PASS, FAIL, UNRESOLVED/not evaluated).
  campaign_assess.py cost WORK --price-in P --price-cached P --price-out P     (measured tokens, hit rate, USD per run, projection)
  campaign_assess.py collect WORK --out DISPOSITIONS.json
      Reads every VALID assessment.json into {"<run>::<item>": "pass"|"fail"|...} for `build_campaign_record.py --dispositions`,
      and lists runs whose assessment is missing or not VALID. It never edits a run directory. Runs are keyed by (command key, run name): a run of a
      replicate set k >= 1 (commands.json `set`) is named `<command>/<run>` in the keys, because its run name repeats set 0's; set 0 keeps the bare
      run name. `--evidence-out F` also writes {"<run>::<item>": evaluator evidence text} (data for the descriptive component table, never a verdict).
  campaign_assess.py run WORK ... --assessment-root RERUN --format-rerun-of PRIMARY      (once-only format rerun)
      Reruns exactly the runs frozen in RERUN/PASS-AUTHORIZATION.json (phase "format-rerun"), each of whose PRIMARY assessment is
      INVALID_SCHEMA or UNPARSEABLE, or is an EXECUTION_ERROR that transport_failure() classifies as a provider transport error (contract
      section 3; listed in the authorization's transport_runs) or that limit_failure() classifies as the evaluator's own wall-clock or turn limit
      (eighth ruling; listed in limit_runs), and still has the frozen digest. Same model, prompt and strict schema. Both outputs are kept; an exclusive
      FORMAT-RERUN-STARTED.json makes the pass once-only. A second failure stays unresolved. Other evaluator execution errors (a clean exit without a result,
      an unclassified failure), inadmissible identities and VALID assessments (including VALID with unresolved items) are never rerun.
  campaign_assess.py collect WORK --out D.json --assessment-root PRIMARY --rerun-root RERUN
      Uses the rerun result only for a primary that is format-invalid or a frozen transport or evaluator-limit failure and frozen in the rerun authorization, and only if the rerun is VALID.
The evaluator model must differ from the executor (assess70 refuses otherwise). Any other rerun of an assessment is not authorized.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import re
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import arms_spec  # noqa: E402
EVAL = HERE.parent / "eval"
ASSESS = EVAL / "assess70.py"
# Panels whose items need a model judgement. Routing, unversioned and burden items are scored by binding oracles or recorded bytes.
DEFAULT_PANELS = ("main", "versioning", "sentinels", "sentinels-add")
FORMAT_INVALID = ("INVALID_SCHEMA", "UNPARSEABLE")        # evaluator output-format failures; the statuses the once-only format rerun covers
TRANSPORT_STATUS = (429, 500, 502, 503, 504)              # provider HTTP errors that the contract section 3 treats as transport (429: stakeholder fourteenth set)
TRANSPORT_STREAM = "stream closed before a finish_reason"  # the interrupted provider stream diagnosed in C(b) transport recovery


def in_panels(d: Path, panels) -> bool:
    key = d.parent.name                              # command key: <panel>-cNN
    return any(key.startswith(p + "-c") and key[len(p) + 2:].isdigit() for p in panels)


def run_dirs(work: Path, panels=DEFAULT_PANELS):
    gated = arms_spec.assessed(arms_spec.load(work))
    for d in sorted((work / "runs").glob("*/*-r*")):
        if (d / "summary.json").exists() and d.name.rsplit("-", 2)[1] in gated and in_panels(d, panels):
            yield d


def one(d: Path, a) -> tuple[str, int]:
    output = assessment_dir(d, a)
    output.mkdir(parents=True, exist_ok=True)
    episode = json.loads((d / "summary.json").read_text())["episode"]
    cmd = [sys.executable, str(ASSESS), "--run", str(d), "--keys", str(a.keys_root / episode),
           "--evaluator-profile", str(a.evaluator_profile), "--evaluator-capabilities", str(a.evaluator_capabilities)]
    if a.shared_rubric:
        cmd += ["--shared-rubric", str(a.shared_rubric)]
    if getattr(a, "assessment_root", None):
        cmd += ["--out-dir", str(output)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    (output / "assessment.stderr.txt").write_text(p.stderr)
    return d.name, p.returncode


def assessment_dir(d: Path, a) -> Path:
    root = getattr(a, "assessment_root", None)
    if root is None:
        return d
    if root.resolve() == (a.work / "evaluations").resolve() or (a.work / "evaluations").resolve() not in root.resolve().parents:
        raise ValueError("assessment-root must be a separate pass under WORK/evaluations/")
    return root / d.relative_to(a.work / "runs")


def check_authorization(a) -> tuple[dict | None, int]:
    root = a.assessment_root
    assessment_dir(a.work / "runs" / "probe", a)
    auth_path = root / "PASS-AUTHORIZATION.json"
    if not auth_path.is_file():
        print("separate assessment pass is not authorized")
        return None, 2
    auth = json.loads(auth_path.read_text())
    for path, key in ((ASSESS, "assess_sha256"), (EVAL / "core70.py", "core_sha256"),
                      (EVAL / "assessment_evidence.py", "assessment_evidence_sha256"),
                      (Path(__file__), "driver_sha256"), (a.evaluator_profile, "profile_sha256")):
        if hashlib.sha256(path.read_bytes()).hexdigest() != auth.get(key):
            print(f"separate assessment pass identity differs: {key}")
            return None, 2
    return auth, 0


SLOT = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+-r[0-9]+")


def slot_of(d: Path, work: Path) -> str:
    return d.relative_to(work / "runs").as_posix()


def error_class(data: dict, path: Path | None = None) -> str:
    """Coarse class of a rerun-eligible failure: transport (a provider transport error, see transport_failure), limit (the evaluator's wall-clock or turn limit, see limit_failure), no-result-text (reported
    separately: may hide a loop or cap), invalid-json, or schema; any other execution error is named by its status."""
    if data.get("assessment_status") == "EXECUTION_ERROR":
        return (exec_class(path) if path is not None else None) or "EXECUTION_ERROR"
    errors = [e for e in data.get("errors", []) if isinstance(e, str)]
    if any(e.startswith("no result text") for e in errors):
        return "no-result-text"
    if any(e.startswith("invalid JSON result") for e in errors):
        return "invalid-json"
    return "schema"


def transport_failure(path: Path) -> bool:
    """True iff an EXECUTION_ERROR primary assessment ended on a provider transport error with no evaluator decision (contract section 3).

    All of: the evaluator process did not time out (return code 124) and returned no result text; the final assistant message in the trace has
    stopReason "error" and either a closed provider stream or a 429/5xx provider status; and that message carries no text and no tool call, so the
    evaluator had emitted no answer or action at the failure point (a stream that drops its finish reason after a streamed answer is not
    transport). A wall-clock timeout, an exhausted turn budget (403) and a clean exit without a result are never transport."""
    try:
        data = json.loads((path / "assessment.json").read_text())
        if data.get("assessment_status") != "EXECUTION_ERROR" or data.get("raw_result"):
            return False
        if any("returncode=124" in e for e in data.get("errors", []) if isinstance(e, str)):
            return False
        last = None
        for line in (path / "assessment-trace.jsonl").read_text().splitlines():
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            msg = rec.get("message") if isinstance(rec, dict) else None
            if rec.get("type") == "message_end" and isinstance(msg, dict) and msg.get("role") == "assistant":
                last = msg
    except (OSError, ValueError, AttributeError):
        return False
    if last is None or last.get("stopReason") != "error" or not isinstance(last.get("content"), list):
        return False
    if any(not isinstance(b, dict) or (b.get("type") == "text" and str(b.get("text", "")).strip()) or "tool" in str(b.get("type", "")).lower()
           for b in last["content"]):
        return False
    text = last.get("errorMessage")
    return (isinstance(text, str) and TRANSPORT_STREAM in text) or last.get("errorStatus") in TRANSPORT_STATUS


def trace_digest(path: Path) -> str | None:
    try:
        return hashlib.sha256((path / "assessment-trace.jsonl").read_bytes()).hexdigest()
    except OSError:
        return None


def limit_failure(path: Path) -> bool:
    """True iff an EXECUTION_ERROR primary assessment ended on the evaluator's own frozen limits with no result (eighth ruling, 2026-10-10):
    the wall-clock limit (return code 124) or the turn budget (a final assistant message refused with status 403 "turn budget"). The
    raw result must be empty. Disjoint from transport_failure(): that needs a closed stream or a 429/5xx status and excludes return code 124."""
    try:
        data = json.loads((path / "assessment.json").read_text())
        if data.get("assessment_status") != "EXECUTION_ERROR" or data.get("raw_result"):
            return False
        if any("returncode=124" in e for e in data.get("errors", []) if isinstance(e, str)):
            return True
        last = None
        for line in (path / "assessment-trace.jsonl").read_text().splitlines():
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            msg = rec.get("message") if isinstance(rec, dict) else None
            if rec.get("type") == "message_end" and isinstance(msg, dict) and msg.get("role") == "assistant":
                last = msg
    except (OSError, ValueError, AttributeError):
        return False
    return (last is not None and last.get("stopReason") == "error" and last.get("errorStatus") == 403
            and "turn budget" in str(last.get("errorMessage", "")))


# EXECUTION_ERROR rerun classes: (class name, authorization key mapping slot -> primary trace sha256, classifier)
EXEC_CLASSES = (("transport", "transport_runs", transport_failure), ("limit", "limit_runs", limit_failure))


def exec_class(path: Path) -> str | None:
    for name, _, test in EXEC_CLASSES:
        if test(path):
            return name
    return None


def format_rerun_slots(a, auth) -> tuple[list[Path] | None, str]:
    """The frozen once-only rerun set, re-verified against the primary pass. Returns (dirs, "") or (None, reason).

    The set must equal every format-invalid primary assessment plus every EXECUTION_ERROR primary that is a provider transport failure
    (those, and only those, are listed in the authorization's transport_runs with each primary trace's sha256), the primary pass must be complete (every COMPLETE_ADMISSIBLE run in the
    panels has an assessment), and the full pass must have been released (evaluator-full.ok)."""
    primary, evaluations = a.format_rerun_of, (a.work / "evaluations").resolve()
    if primary.resolve() == a.assessment_root.resolve() or primary.resolve().parent != evaluations:
        return None, "format-rerun-of must be a different pass directly under WORK/evaluations/"
    if auth.get("source_root") != primary.name or not isinstance(auth.get("runs"), dict) or not auth["runs"]:
        return None, "format-rerun authorization does not bind this primary root and a frozen run set"
    if auth.get("panels") != list(a.panels):
        return None, "format-rerun authorization panels differ from --panels"
    if not (a.work / "authorizations" / "evaluator-full.ok").exists():
        return None, "the full primary pass was not released (authorizations/evaluator-full.ok)"
    declared = {key: auth.get(key, {}) for _, key, _ in EXEC_CLASSES}
    if not all(isinstance(m, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in m.items()) for m in declared.values()):
        return None, "transport_runs and limit_runs must map run slots to the sha256 of each primary assessment trace"
    found, by_class = set(), {name: set() for name, _, _ in EXEC_CLASSES}
    for d in run_dirs(a.work, a.panels):
        if json.loads((d / "summary.json").read_text())["evidence_state"] != "COMPLETE_ADMISSIBLE":
            continue
        slot = slot_of(d, a.work)
        path = primary / slot / "assessment.json"
        if not path.is_file():
            return None, f"the primary pass is incomplete: no assessment for {slot}"
        if json.loads(path.read_text()).get("assessment_status") in FORMAT_INVALID:
            found.add(slot)
        elif exec_class(path.parent):
            found.add(slot)
            by_class[exec_class(path.parent)].add(slot)
    if found != set(auth["runs"]) or any(by_class[name] != set(declared[key]) for name, key, _ in EXEC_CLASSES):
        return None, "the frozen run set is not exactly the format-invalid, provider-transport and evaluator-limit primary assessments"
    for name, key, _ in EXEC_CLASSES:
        for slot in sorted(by_class[name]):
            if trace_digest(primary / slot) != declared[key][slot]:
                return None, f"primary trace for {slot} differs from the frozen digest"
    dirs = []
    for slot, digest in sorted(auth["runs"].items()):
        if not isinstance(slot, str) or not SLOT.fullmatch(slot) or ".." in slot.split("/"):
            return None, f"malformed run slot {slot!r}"
        run = a.work / "runs" / slot
        path = primary / slot / "assessment.json"
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            return None, f"primary assessment for {slot} differs from the frozen digest"
        dirs.append(run)
    return dirs, ""


def viable(a, todo) -> str:
    """Everything the provider launch needs, checked before the once-only marker is consumed."""
    if a.keys_root is None or a.evaluator_capabilities is None or not Path(a.evaluator_capabilities).is_file():
        return "keys root or evaluator capabilities file is missing"
    if a.shared_rubric is not None and not Path(a.shared_rubric).is_file():
        return "shared rubric file is missing"
    for d in todo:
        episode = json.loads((d / "summary.json").read_text()).get("episode")
        if not isinstance(episode, str) or not (Path(a.keys_root) / episode).is_dir():
            return f"no custodian key directory for {d.name}"
    return ""


def cmd_format_rerun(a) -> int:
    if a.assessment_root is None or a.limit:
        print("format rerun needs a separate --assessment-root and takes no --limit")
        return 2
    try:
        auth, rc = check_authorization(a)
        if rc:
            return rc
        if auth.get("phase") != "format-rerun":
            print("separate assessment pass is not released for a format rerun")
            return 2
        todo, why = format_rerun_slots(a, auth)
        if todo is None:
            print(why)
            return 2
        if any(assessment_dir(d, a).exists() for d in todo):
            print("a rerun output already exists; the format rerun is once-only")
            return 2
    except ValueError as exc:
        print(f"refused: {exc}")
        return 2
    if not os.environ.get("SSDP70_OMP_PROVIDER_CREDENTIAL"):
        print("SSDP70_OMP_PROVIDER_CREDENTIAL is not set", file=sys.stderr)
        return 2
    why = viable(a, todo)
    if why:
        print(why)
        return 2
    try:
        with open(a.assessment_root / "FORMAT-RERUN-STARTED.json", "x") as fh:                 # exclusive: durable once-only marker, before any provider call
            json.dump({"runs": sorted(auth["runs"]), "authorization_sha256": hashlib.sha256((a.assessment_root / "PASS-AUTHORIZATION.json").read_bytes()).hexdigest()}, fh)
    except FileExistsError:
        print("FORMAT-RERUN-STARTED.json exists; the format rerun is once-only")
        return 2
    print(f"{len(todo)} runs to rerun")
    bad = 0

    def attempt(d):
        try:
            return one(d, a)
        except Exception as exc:                                                              # no retry: the run stays unresolved and the driver exits 3
            return d.name, f"exception {type(exc).__name__}"
    with cf.ThreadPoolExecutor(max_workers=a.parallel) as pool:
        for name, rc in pool.map(attempt, todo):
            print(f"{name}: assess70 exit {rc}")
            if rc not in (0, 1, 2):
                bad += 1
    return 3 if bad else 0


def cmd_run(a) -> int:
    if getattr(a, "format_rerun_of", None) is not None:
        return cmd_format_rerun(a)
    root = getattr(a, "assessment_root", None)
    if root is not None:
        auth, rc = check_authorization(a)
        if rc:
            return rc
        if auth.get("phase") == "pilot" and a.limit != 5:
            print("separate assessment pass is released only for five pilot sessions")
            return 2
        if auth.get("phase") not in ("pilot", "full"):
            print("separate assessment pass phase is not released")
            return 2
    if not os.environ.get("SSDP70_OMP_PROVIDER_CREDENTIAL"):
        print("SSDP70_OMP_PROVIDER_CREDENTIAL is not set", file=sys.stderr)
        return 2
    if not a.limit and not (a.work / "authorizations" / "evaluator-full.ok").exists():
        print("the full evaluator pass is not authorized: run the pilot (--limit) and wait for authorizations/evaluator-full.ok", file=sys.stderr)
        return 2
    todo = [d for d in run_dirs(a.work, a.panels)
            if json.loads((d / "summary.json").read_text())["evidence_state"] == "COMPLETE_ADMISSIBLE" and not (assessment_dir(d, a) / "assessment.json").exists()]
    if root is not None and auth["phase"] == "pilot":
        pilot = auth.get("pilot_runs", [])
        if len(pilot) != 5 or len(set(pilot)) != 5:
            print("separate pilot lacks five frozen run slots")
            return 2
        todo = [d for d in todo if d.relative_to(a.work / "runs").as_posix() in pilot]
    if a.limit:
        todo = todo[:a.limit]
    print(f"{len(todo)} runs to assess")
    bad = 0
    with cf.ThreadPoolExecutor(max_workers=a.parallel) as pool:
        for name, rc in pool.map(lambda d: one(d, a), todo):
            print(f"{name}: assess70 exit {rc}")
            if rc not in (0, 1, 2):
                bad += 1
    return 3 if bad else 0


def identity_of(path: Path):
    try:
        return json.loads((path / "assessment-identity.json").read_text()).get("identity_sha256")
    except (OSError, ValueError):
        return None


def cmd_collect(a) -> int:
    out, problems, n, used, first, rows = {}, [], 0, [], [], []
    rerun_root = getattr(a, "rerun_root", None)
    frozen, marked, exec_frozen = {}, False, {}
    sets, evidence = arms_spec.command_sets(a.work), {}
    if rerun_root is not None:
        if getattr(a, "assessment_root", None) is None:
            print("--rerun-root needs the primary --assessment-root")
            return 2
        auth_path = rerun_root / "PASS-AUTHORIZATION.json"
        auth = json.loads(auth_path.read_text()) if auth_path.is_file() else {}
        if auth.get("phase") not in ("format-rerun", "format-rerun-complete") or auth.get("source_root") != a.assessment_root.name:
            print("rerun root is not an authorized format rerun of this primary root")
            return 2
        if auth.get("panels") != list(a.panels):
            print("rerun authorization panels differ from --panels")
            return 2
        frozen = auth.get("runs", {})
        for name, key, _ in EXEC_CLASSES:
            if isinstance(auth.get(key), dict):
                exec_frozen.update({slot: (name, trace) for slot, trace in auth[key].items()})
        try:
            marker = json.loads((rerun_root / "FORMAT-RERUN-STARTED.json").read_text())
            marked = marker.get("authorization_sha256") == hashlib.sha256(auth_path.read_bytes()).hexdigest() and marker.get("runs") == sorted(frozen)
        except (OSError, ValueError):
            marked = False
    for d in run_dirs(a.work, a.panels):
        if json.loads((d / "summary.json").read_text())["evidence_state"] != "COMPLETE_ADMISSIBLE":
            continue
        n += 1
        rid = arms_spec.run_id(d.name, d.parent.name, sets.get(d.parent.name, 0))
        path = assessment_dir(d, a) / "assessment.json"
        if not path.exists():
            problems.append({"run": rid, "what": "no assessment"})
            continue
        data = json.loads(path.read_text())
        slot = slot_of(d, a.work)
        if data.get("assessment_status") in FORMAT_INVALID or (data.get("assessment_status") == "EXECUTION_ERROR" and slot in exec_frozen):
            row = {"run": rid, "panel": slot.split("/")[0], "arm": d.name.rsplit("-", 2)[1], "first_status": data["assessment_status"],
                   "first_class": error_class(data, path.parent), "first_items": sorted(set(re.findall(r"item (\S+) ", " ".join(e for e in data.get("errors", []) if isinstance(e, str)))))}
            first.append(row)
            rerun = (rerun_root / slot / "assessment.json") if rerun_root is not None else None
            if rerun_root is None:
                problems.append({"run": rid, "what": f"assessment {data['assessment_status']}", "first_class": row["first_class"]})
                continue
            if slot not in frozen or hashlib.sha256(path.read_bytes()).hexdigest() != frozen[slot]:
                problems.append({"run": rid, "what": "rerun-eligible primary (format-invalid, transport or limit) is not in the frozen rerun set"})
                continue
            if not marked:
                problems.append({"run": rid, "what": "format rerun marker missing or does not match the authorization"})
                continue
            if slot in exec_frozen and (trace_digest(path.parent) != exec_frozen[slot][1] or exec_class(path.parent) != exec_frozen[slot][0]):
                problems.append({"run": rid, "what": f"{exec_frozen[slot][0]} primary does not match its frozen trace digest or classification"})
                continue
            if not rerun.exists():
                problems.append({"run": rid, "what": "format rerun missing", "first_class": row["first_class"]})
                continue
            if identity_of(rerun.parent) is None or identity_of(rerun.parent) != identity_of(path.parent):
                problems.append({"run": rid, "what": "rerun assessment identity differs from the primary's"})
                continue
            data = json.loads(rerun.read_text())
            row["rerun_status"] = data.get("assessment_status")
            row["rerun_class"] = (None if data.get("assessment_status") == "VALID" else error_class(data, rerun.parent) if data.get("assessment_status") in FORMAT_INVALID + ("EXECUTION_ERROR",)
                                  else str(data.get("assessment_status")))            # an EXECUTION_ERROR/INADMISSIBLE rerun is never a same-class format failure
            rows.append(row)
            used.append(slot)
            if data.get("assessment_status") != "VALID":
                problems.append({"run": rid, "what": f"format rerun {data.get('assessment_status')}", "first_class": row["first_class"], "rerun_class": row["rerun_class"]})
                continue
        if data.get("assessment_status") != "VALID":
            problems.append({"run": rid, "what": f"assessment {data.get('assessment_status')}"})
            continue
        for disp in data["dispositions"]:
            out[f"{rid}::{disp['item'].split('::', 1)[-1]}"] = disp["result"]
            evidence[f"{rid}::{disp['item'].split('::', 1)[-1]}"] = disp.get("evidence", "")
    a.out.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    if getattr(a, "evidence_out", None):
        a.evidence_out.write_text(json.dumps(evidence, indent=1, sort_keys=True) + "\n")

    def tally(key, items):
        t = {}
        for r in items:
            t[r[key]] = t.get(r[key], 0) + 1
        return dict(sorted(t.items()))
    item_counts = {}
    for r in first:
        for i in r["first_items"]:
            m = i.split("::", 1)[-1]
            item_counts[m] = item_counts.get(m, 0) + 1
    report = {"first_draw_format_failures": sum(r["first_class"] not in ("transport", "limit") for r in first),
              "first_draw_transport_failures": sum(r["first_class"] == "transport" for r in first),
              "first_draw_limit_failures": sum(r["first_class"] == "limit" for r in first), "by_arm": tally("arm", first), "by_panel": tally("panel", first),
              "by_status": tally("first_status", first), "by_class": tally("first_class", first), "items_named_in_errors": dict(sorted(item_counts.items())),
              "reruns_attempted": len(rows), "reruns_valid": sum(r["rerun_status"] == "VALID" for r in rows),
              "reruns_second_invalid": sum(r["rerun_status"] != "VALID" for r in rows),
              "second_invalid_same_class_as_first": sum(r["rerun_status"] in FORMAT_INVALID + ("EXECUTION_ERROR",) and r["rerun_class"] == r["first_class"] for r in rows),
              "reruns_second_not_format_invalid": sum(r["rerun_status"] not in ("VALID",) + FORMAT_INVALID for r in rows),
              "reruns_missing_or_rejected": len([x for x in problems if x["what"].startswith(("format rerun missing", "format rerun marker", "rerun assessment identity"))]),
              "second_invalid_by_arm": tally("arm", [r for r in rows if r["rerun_status"] != "VALID"]),
              "rows": sorted(rows, key=lambda r: r["run"])}
    print(json.dumps({"admissible_runs": n, "dispositions": len(out), "format_reruns_used": used, "format_failure_report": report, "problems": problems}, indent=1))
    return 0 if not problems else 4


def trace_usage(path: Path) -> dict:
    tot = {"input": 0, "cacheRead": 0, "output": 0, "turns": 0}
    for line in path.read_text().splitlines():
        if '"message_end"' not in line:
            continue
        try:
            o = json.loads(line)
        except ValueError:
            continue
        m = o.get("message", {})
        if o.get("type") == "message_end" and m.get("role") == "assistant" and isinstance(m.get("usage"), dict):
            tot["turns"] += 1
            for k in ("input", "cacheRead", "output"):
                tot[k] += int(m["usage"].get(k, 0))
    return tot


def cmd_cost(a) -> int:
    """Measured evaluator tokens and dollars (from assessment-trace.jsonl) and the projection to every evaluable run."""
    done = [assessment_dir(d, a) for d in run_dirs(a.work, a.panels) if (assessment_dir(d, a) / "assessment-trace.jsonl").exists()]
    if not done:
        print("no assessed runs yet")
        return 2
    rows = [trace_usage(d / "assessment-trace.jsonl") for d in done]
    total = {k: sum(r[k] for r in rows) for k in rows[0]}

    def dollars(r):
        return (r["input"] * a.price_in + r["cacheRead"] * a.price_cached + r["output"] * a.price_out) / 1e6

    per = dollars(total) / len(rows)
    assessed = arms_spec.assessed(arms_spec.load(a.work))
    gated = sum(c["runs"] // len(c["arms"]) * len([x for x in c["arms"] if x in assessed]) if c.get("arms") else c["runs"]
                for c in json.loads((a.work / "commands.json").read_text())["commands"] if c["panel"] in a.panels and not c.get("conditional"))
    hit = total["cacheRead"] / max(1, total["cacheRead"] + total["input"])
    out = {"assessed_runs": len(rows), "mean_turns": round(total["turns"] / len(rows), 1),
           "mean_tokens": {k: round(total[k] / len(rows)) for k in ("input", "cacheRead", "output")},
           "cache_hit_rate": round(hit, 3), "mean_usd_per_run": round(per, 4), "planned_evaluable_runs": gated,
           "projected_usd": round(per * gated, 2)}
    print(json.dumps(out, indent=1))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    c = sub.add_parser("collect")
    for sp in (r, c):
        sp.add_argument("work", type=Path)
    r.add_argument("--keys-root", type=Path, required=True)
    r.add_argument("--evaluator-profile", type=Path, required=True)
    r.add_argument("--evaluator-capabilities", type=Path, required=True)
    r.add_argument("--shared-rubric", type=Path)
    r.add_argument("--parallel", type=int, default=4)
    r.add_argument("--limit", type=int, help="assess only the first N runs (the pilot)")
    r.add_argument("--format-rerun-of", type=Path, help="once-only rerun of the format-invalid assessments of this primary root (see module doc)")
    c.add_argument("--rerun-root", type=Path, help="format-rerun root whose VALID results replace frozen format-invalid primaries")
    c.add_argument("--out", type=Path, required=True)
    c.add_argument("--evidence-out", type=Path, help="also write {run::item: evaluator evidence text} (descriptive input for compare_721.py)")
    k = sub.add_parser("cost")
    k.add_argument("work", type=Path)
    k.add_argument("--price-in", type=float, required=True, help="USD per million uncached input tokens")
    k.add_argument("--price-cached", type=float, required=True)
    k.add_argument("--price-out", type=float, required=True)
    for sp in (r, c, k):
        sp.add_argument("--panels", nargs="+", default=list(DEFAULT_PANELS))
        sp.add_argument("--assessment-root", type=Path, help="Use a separate assessment pass under WORK/evaluations/")
    a = ap.parse_args()
    return {"run": cmd_run, "collect": cmd_collect, "cost": cmd_cost}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
