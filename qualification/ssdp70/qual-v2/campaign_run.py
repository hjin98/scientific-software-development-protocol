#!/usr/bin/env python3
"""Sequential campaign runner for the operator (launches live runs only when the operator starts it from their own terminal).

  campaign_run.py WORK start [STAGE]     needs SSDP70_OMP_PROVIDER_CREDENTIAL; runs the unconditional commands of one stage (default 1:
                                          the main panel) one after another (so at most --parallel runs are in flight), detached in
                                          its own session. Stage 2 (the Q5 panels) starts only if the analyst wrote authorizations/stage2.ok
                                          after verifying stage 1. Staging is ordering only; no candidate gate is scored between stages.
  campaign_run.py WORK status             per command: NOT-LAUNCHED | RUNNING | EXIT <rc> | CRASHED; runs started and summaries so far
  campaign_run.py WORK run-conditional KEY   runs one conditional command; only if WORK/authorizations/KEY.ok exists (written by the analyst)
  campaign_run.py WORK run-rerun STAGE    runs the analyst's frozen rerun plan WORK/rerun-commands-stage<STAGE>.json (prepare_campaign.py
                                          plan-rerun) sequentially, detached, once; needs READY "RERUN MAY START" and
                                          WORK/authorizations/rerun-stage<STAGE>.ok containing that plan's sha256

A command that exits 0 or 2 (2 = at least one run is not admissible) lets the sequence continue. Any other exit code, or a crash,
writes WORK/launch/HALT and stops the sequence. The runner never reruns, never edits a run directory and never deletes anything.
Rerunning a lost run is the analyst's decision (contract section 3): the analyst freezes a rerun plan into a new directory and authorizes it.
The arms specification (WORK/arms-spec.json, arms_spec.py) is read as a guard: `start` and `run-conditional` refuse a commands.json that names an
arm outside it, and `status` prints each panel's replicate set per command (`set`).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arms_spec  # noqa: E402

CONTINUE = (0, 2)


def commands(work: Path) -> list[dict]:
    return json.loads((work / "commands.json").read_text())["commands"]


def spec_problem(work: Path) -> str:
    """A command naming an arm outside the arms specification (empty string when the plan agrees with it)."""
    spec = arms_spec.load(work)
    names = set(arms_spec.label_of(spec))
    bad = sorted({a for c in commands(work) for a in c["arms"]} - names)
    if bad:
        return f"commands.json names arms outside the arms specification: {bad}"
    if (work / arms_spec.SPEC_NAME).is_file():
        mismatched = [c["key"] for c in commands(work) if c["arms"] != arms_spec.panel_arms(spec, c["panel"])]
        if mismatched:
            return f"commands.json panel arms differ from the arms specification: {mismatched}"
    return ""


def state(work: Path, key: str) -> str:
    base = work / "launch" / key
    if base.with_suffix(".exit").exists():
        return f"EXIT {base.with_suffix('.exit').read_text().strip()}"
    pid = base.with_suffix(".pid")
    if pid.exists():
        try:
            os.kill(int(pid.read_text()), 0)
            return "RUNNING"
        except (OSError, ValueError):
            return "CRASHED"
    return "NOT-LAUNCHED"


def run_one(work: Path, c: dict) -> int:
    launch = work / "launch"
    launch.mkdir(parents=True, exist_ok=True)
    key = c["key"]
    (launch / f"{key}.started").write_text(time.strftime("%FT%TZ", time.gmtime()) + "\n")
    log = open(launch / f"{key}.log", "ab")
    proc = subprocess.Popen(c["argv"], stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    (launch / f"{key}.pid").write_text(str(proc.pid))
    rc = proc.wait()
    (launch / f"{key}.exit").write_text(f"{rc}\n")
    return rc


def rerun_commands(work: Path, stage: int) -> list[dict]:
    path = work / f"rerun-commands-stage{stage}.json"
    return json.loads(path.read_text())["commands"] if path.exists() else []


def rerun_loop(work: Path, stage: int) -> None:
    (work / "launch" / f"rerun-runner-stage{stage}.pid").write_text(str(os.getpid()))
    for c in rerun_commands(work, stage):
        if state(work, c["key"]) != "NOT-LAUNCHED":
            continue
        rc = run_one(work, c)
        if rc not in CONTINUE:
            (work / "launch" / "HALT").write_text(f"{c['key']} exited {rc}\n")
            return
    (work / "launch" / f"DONE-rerun-stage{stage}").write_text(time.strftime("%FT%TZ", time.gmtime()) + "\n")


def loop(work: Path, stage: int) -> None:
    (work / "launch" / f"runner-stage{stage}.pid").write_text(str(os.getpid()))
    for c in commands(work):
        if c.get("conditional") or int(c.get("stage", 1)) != stage:
            continue
        if state(work, c["key"]) != "NOT-LAUNCHED":
            continue
        rc = run_one(work, c)
        if rc not in CONTINUE:
            (work / "launch" / "HALT").write_text(f"{c['key']} exited {rc}\n")
            return
    (work / "launch" / f"DONE-stage{stage}").write_text(time.strftime("%FT%TZ", time.gmtime()) + "\n")


def counts(work: Path, key: str) -> tuple[int, int, int]:
    d = work / "runs" / key
    return (len(list(d.glob("*-r*/"))) if d.exists() else 0, len(list(d.glob("*-r*/summary.json"))) if d.exists() else 0,
            len(list(d.glob("*.error.txt"))) if d.exists() else 0)


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    work, action = Path(sys.argv[1]).resolve(), sys.argv[2]
    if action == "_loop":
        loop(work, int(sys.argv[3]))
        return 0
    if action == "_rerun_loop":
        rerun_loop(work, int(sys.argv[3]))
        return 0
    if action == "run-rerun":
        if not os.environ.get("SSDP70_OMP_PROVIDER_CREDENTIAL"):
            print("SSDP70_OMP_PROVIDER_CREDENTIAL is not set", file=sys.stderr)
            return 2
        stage = int(sys.argv[3])
        plan = work / f"rerun-commands-stage{stage}.json"
        ready = (work / "READY").read_text() if (work / "READY").exists() else ""
        auth = work / "authorizations" / f"rerun-stage{stage}.ok"
        if "RERUN MAY START" not in ready:
            print("READY does not say 'RERUN MAY START'; the analyst has not released the rerun", file=sys.stderr)
            return 2
        if not plan.exists() or not auth.exists() or hashlib.sha256(plan.read_bytes()).hexdigest() not in auth.read_text():
            print(f"the rerun of stage {stage} is not authorized: authorizations/{auth.name} must name the sha256 of {plan.name}", file=sys.stderr)
            return 2
        if not (work / "launch" / f"DONE-stage{stage}").exists():
            print(f"stage {stage} has not finished (no DONE-stage{stage})", file=sys.stderr)
            return 2
        if (work / "launch" / f"rerun-runner-stage{stage}.pid").exists() or (work / "launch" / "HALT").exists():
            print("a rerun runner was already started or halted here; do not relaunch", file=sys.stderr)
            return 2
        if (work / "launch" / f"runner-stage{stage + 1}.pid").exists():
            print(f"stage {stage + 1} was already started; the stage {stage} rerun must run before it", file=sys.stderr)
            return 2
        if spec_problem(work) or {c["arm"] for c in rerun_commands(work, stage)} - {a for c in commands(work) for a in c["arms"]}:
            print("the rerun plan names an arm outside the plan or the arms specification", file=sys.stderr)
            return 2
        proc = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), str(work), "_rerun_loop", str(stage)], start_new_session=True,
                                stdout=open(work / "launch" / "runner.log", "ab"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        print(f"started the sequential rerun runner for stage {stage} (pid {proc.pid})")
        return 0
    if action == "start":
        if not os.environ.get("SSDP70_OMP_PROVIDER_CREDENTIAL"):
            print("SSDP70_OMP_PROVIDER_CREDENTIAL is not set", file=sys.stderr)
            return 2
        stage = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        if spec_problem(work):
            print(spec_problem(work), file=sys.stderr)
            return 2
        ready = (work / "READY").read_text() if (work / "READY").exists() else ""
        need = "OPERATOR MAY LAUNCH" if stage == 1 else "STAGE 2 MAY START"
        if need not in ready:
            print(f"READY does not say {need!r}; the analyst has not released this stage", file=sys.stderr)
            return 2
        if stage > 1 and not (work / "authorizations" / f"stage{stage}.ok").exists():
            print(f"stage {stage} is not authorized: the analyst has not written authorizations/stage{stage}.ok", file=sys.stderr)
            return 2
        if stage > 1 and not (work / "launch" / f"DONE-stage{stage - 1}").exists():
            print(f"stage {stage - 1} has not finished (no DONE-stage{stage - 1})", file=sys.stderr)
            return 2
        if (work / "launch" / f"runner-stage{stage}.pid").exists() or (work / "launch" / "HALT").exists():
            print("a runner was already started or halted here; do not relaunch; see the hand-off, section on halts", file=sys.stderr)
            return 2
        if stage > 1 and (work / "launch" / f"rerun-runner-stage{stage - 1}.pid").exists() and not (work / "launch" / f"DONE-rerun-stage{stage - 1}").exists():
            print(f"the stage {stage - 1} rerun has not finished (no DONE-rerun-stage{stage - 1})", file=sys.stderr)
            return 2
        (work / "launch").mkdir(parents=True, exist_ok=True)
        proc = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), str(work), "_loop", str(stage)], start_new_session=True,
                                stdout=open(work / "launch" / "runner.log", "ab"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        print(f"started the sequential runner for stage {stage} (pid {proc.pid})")
        return 0
    if action == "status":
        for c in commands(work):
            started, summaries, errors = counts(work, c["key"])
            print(f"{c['key']:<18} stage {c.get('stage', 1)} {'(conditional) ' if c.get('conditional') else ''}{'set ' + str(c['set']) + ' ' if 'set' in c else ''}{state(work, c['key']):<14} "
                  f"started {started:>3} summaries {summaries:>3} of {c['runs']:>3}  error files {errors}")
        for stage in (1, 2):
            for c in rerun_commands(work, stage):
                d = work / "runs" / f"rerun-s{stage}-{c['arm']}" / c["source_command"]
                summaries = len(list(d.glob("*-r*/summary.json"))) if d.exists() else 0
                print(f"{c['key']:<30} rerun {state(work, c['key']):<14} summaries {summaries:>3} of {c['runs']:>3}")
        for flag in ("HALT", "DONE-stage1", "DONE-stage2", "DONE-rerun-stage1", "DONE-rerun-stage2"):
            if (work / "launch" / flag).exists():
                print(flag, (work / "launch" / flag).read_text().strip())
        return 0
    if action == "run-conditional":
        key = sys.argv[3]
        c = next((x for x in commands(work) if x["key"] == key), None)
        if c is None or not c.get("conditional"):
            print(f"{key} is not a conditional command", file=sys.stderr)
            return 2
        if spec_problem(work):
            print(spec_problem(work), file=sys.stderr)
            return 2
        if not (work / "authorizations" / f"{key}.ok").exists():
            print(f"{key} is not authorized: the analyst has not written authorizations/{key}.ok", file=sys.stderr)
            return 2
        if not os.environ.get("SSDP70_OMP_PROVIDER_CREDENTIAL"):
            print("SSDP70_OMP_PROVIDER_CREDENTIAL is not set", file=sys.stderr)
            return 2
        if state(work, key) != "NOT-LAUNCHED":
            print(f"{key} was already launched: {state(work, key)}", file=sys.stderr)
            return 2
        return run_one(work, c)
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
