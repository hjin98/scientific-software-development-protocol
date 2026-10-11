#!/usr/bin/env python3
"""Campaign preparation (analyst tool; provider-free; launches nothing and opens no custody store except the paths you pass).

  init          arms (candidate p72, B1 p66, B2 p66b, 6.5 p65), the executor key, optionally the evaluator key, campaign-identity.json
  static        the pre-live static pre-measurement of the Q5c rule (contract section 5): candidate bytes against the historical
                6.5 baselines with the 512 B margin; writes static-premeasurement.json
  check-corpus  provider-free checks of the custodian's corpus, requirements, oracles and slot flags against the arms and the key
  plan          commands.json (sequential harness `matrix` chunks, panel-driven arms, conditional add-on panels held back),
                declaration.json for build_campaign_record.py, expected-runs.json
  check-plan    provider-free check that the plan resolves (arms, key, episodes, requirements, oracles, counts)
  verify        audits completed runs against the plan with build_campaign_record.py (no scoring)
  freeze-evaluator  freezes the evaluator profile (--model) in an existing campaign directory and records it in the identity
  preflight     OK or STOP per check for the operator (READY, digests, tool hashes, plan, binaries, disk, credential presence)
  report        writes OPERATOR-REPORT.md (status, identity, verification, authorizations, escalations)
  refresh-identity  re-records tool hashes and the repo head in campaign-identity.json after analyst-tool changes (arms and key re-verified)

Stages (ordering only): stage 1 is the main panel (Q1 to Q4), stage 2 the Q5 panels; stage 2 starts only after the
analyst has verified stage 1 and written authorizations/stage2.ok. No candidate gate is scored between stages.
Panels and arms (override with --config): main/routing/versioning/r2/ordinary -> p72 p66 p66b; burden -> p72 p65;
sentinels/unversioned -> p72. A panel named `<base>-add` is conditional: it uses the base arms and is never run by the runner
until the analyst authorizes it (T7 added pairs, Q5e and Q5f extra runs).
Usage: prepare_campaign.py <command> --work WORK [options]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EVAL = REPO / "qualification" / "ssdp70" / "eval"
sys.path[:0] = [str(EVAL), str(REPO / "qualification" / "ssdp70" / "s4")]
import build_s4_probe  # noqa: E402
import core70  # noqa: E402
import harness70  # noqa: E402
import prepare_arms70  # noqa: E402
from adapters import omp, omp_eval  # noqa: E402

CANDIDATE_REF = "2dedcfa3408f62bc11a696ac3776183a87b40438"
B_REF = "22f4bdba53795da3a6f13f162529f3a843fc37ae"       # accepted 6.6.0, PROTOCOL-RELEASE-STATE.yaml
OLD_REF = "7f7b5e24858e813e45ace867a7f8ea5180f43bf0"     # 6.5.0 public source, same file
ARMS = [("p72", CANDIDATE_REF, "7.2.0"), ("p66", B_REF, "6.6.0"), ("p66b", B_REF, "6.6.0"), ("p65", OLD_REF, "6.5.0")]
LABELS = {"p72": "cand", "p66": "b1", "p66b": "b2", "p65": "b65"}
THREE = ["p72", "p66", "p66b"]
PANEL_ARMS = {"main": THREE, "routing": THREE, "versioning": THREE, "r2": THREE, "ordinary": THREE,
              "burden": ["p72", "p65"], "sentinels": ["p72"], "unversioned": ["p72"]}
ROUTES = ["T1", "T7", "T8"]
CHUNK, PARALLEL_MAX = 16, 8
STATIC_BASELINES = {"entry": 8360, "owner": 25188}          # historical 6.5 planning figures (Q5C-STATIC-PREMEASUREMENT-2026-10-07.md)
MARGIN = 512
EVALUATOR_PROVIDER = "deepinfra"
EVALUATOR_TURNS = 20                                   # the committed template allows 40; a cap bounds the context re-sent each turn


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_arms(work: Path):
    arms, manifest_sha = harness70.load_arms_manifest(work / "arms" / "arms.json")
    return arms, manifest_sha


def executor(work: Path):
    return core70.load_profile(work / "keys" / "omp-primary-flash-executor-main.json",
                               work / "keys" / "omp-primary-flash-executor-main.capabilities.json")


def build_evaluator_key(work: Path, model_id: str) -> None:
    exec_model = executor(work).profile["agent_model"]
    full = f"{EVALUATOR_PROVIDER}/{model_id}"
    if full == exec_model:
        sys.exit(f"refused: the evaluator model must not be the executor model ({exec_model}); contract section 3, assess70.py enforces it")
    template = json.loads((EVAL / "profiles" / "omp-evaluator-readonly.template.json").read_text())
    source = json.loads((EVAL / "profiles" / "omp-evaluator-readonly.json").read_text())
    route = dict(source["containment_policy"]["provider_route"])
    route["model_id"] = model_id
    profile = omp_eval.freeze_profile(template, executable_path=str(Path.home() / ".local/bin/omp"), provider_route=route,
                                 reasoning=source["reasoning_configuration"], profile_id="omp-evaluator-readonly",
                                 budgets={"max_turns": EVALUATOR_TURNS, "timeout_s": 1800})
    errors = omp_eval.eval_profile_errors(profile) + omp.runtime_dependency_errors(profile)
    if errors:
        sys.exit(f"evaluator profile refused: {errors}")
    write_json(work / "keys" / "omp-evaluator-readonly.json", profile)
    caps_src = EVAL / "capabilities" / "omp-evaluator-readonly.json"
    (work / "keys" / "omp-evaluator-readonly.capabilities.json").write_bytes(caps_src.read_bytes())


def cmd_init(a) -> int:
    work = a.work
    if (work / "campaign-identity.json").exists() or (work / "arms").exists():
        sys.exit(f"refusing to overwrite {work}")
    if not any(r.resolve() in work.resolve().parents for r in omp.RUN_REALIZATION_ROOTS):
        sys.exit(f"{work} is not beneath an approved OMP realization root")
    drift = subprocess.run(["git", "-C", str(REPO), "diff", "--stat", a.candidate_ref, "HEAD", "--", "source", "dist"],
                           capture_output=True, text=True).stdout.strip()
    if drift:
        sys.exit("the candidate source or dist differs from the frozen identity; this is a new identity (PEM FF-001):\n" + drift)
    records = []
    for name, ref, version in [(n, a.candidate_ref if n == "p72" else r, v) for n, r, v in ARMS]:
        records.append(prepare_arms70.extract_arm(REPO, work / "arms", name, ref, version))
    write_json(work / "arms" / "arms.json", {"schema": 1, "repo": str(REPO), "arms": records})
    profile, caps = build_s4_probe.build_key(work)
    bundle = core70.load_profile(profile, caps)
    errors = omp.profile_errors(bundle.profile)
    if errors:
        sys.exit(f"executor key is not admissible: {errors}")
    if a.evaluator_model:
        build_evaluator_key(work, a.evaluator_model)
    ident = {"schema": 1, "created": subprocess.run(["date", "-u", "+%FT%TZ"], capture_output=True, text=True).stdout.strip(),
             "repo_head": subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
             "candidate_ref": a.candidate_ref, "candidate_source_dist_diff_from_ref": "empty",
             "arms": {r["name"]: {k: r[k] for k in ("commit", "version", "dist_tree_sha256")} for r in records},
             "executor_agent_model": bundle.profile["agent_model"], "executor_profile_sha256": sha(profile),
             "executor_profile_key_sha256": bundle.profile_key_sha256, "executor_budgets": bundle.profile["budgets"],
             "evaluator_profile": ("frozen" if a.evaluator_model else "NOT FROZEN: no evaluator model named"),
             "harness_sha256": sha(EVAL / "harness70.py"), "assess_sha256": sha(EVAL / "assess70.py"), "core_sha256": sha(EVAL / "core70.py"),
             "assessment_evidence_sha256": sha(EVAL / "assessment_evidence.py"),
             "builder_sha256": sha(HERE / "build_campaign_record.py"), "h4_sha256": sha(HERE / "h4.py"),
             "prepare_campaign_sha256": sha(Path(__file__).resolve())}
    write_json(work / "campaign-identity.json", ident)
    print(json.dumps(ident, indent=1))
    return 0


def cmd_refresh_identity(a) -> int:
    """Re-record the tool hashes and repo head after the analyst tools changed; arms and the executor key are re-verified, never rebuilt."""
    path = a.work / "campaign-identity.json"
    ident = json.loads(path.read_text())
    arms, _ = load_arms(a.work)
    for name, row in arms.items():
        harness70.resolve_arm_dist(row)                               # digest re-verified
        if ident["arms"][name]["dist_tree_sha256"] != row["dist_tree_sha256"]:
            sys.exit(f"arm {name} differs from the recorded identity")
    bundle = executor(a.work)
    if sha(a.work / "keys" / "omp-primary-flash-executor-main.json") != ident["executor_profile_sha256"]:
        sys.exit("the executor profile differs from the recorded identity")
    drift = subprocess.run(["git", "-C", str(REPO), "diff", "--stat", ident["candidate_ref"], "HEAD", "--", "source", "dist"],
                           capture_output=True, text=True).stdout.strip()
    if drift:
        sys.exit("the candidate source or dist differs from the frozen identity; this is a new identity (PEM FF-001)")
    old = {k: ident[k] for k in ("repo_head", "harness_sha256", "assess_sha256", "builder_sha256", "h4_sha256", "prepare_campaign_sha256")}
    ident.setdefault("refreshes", []).append({"at": subprocess.run(["date", "-u", "+%FT%TZ"], capture_output=True, text=True).stdout.strip(), "previous": old})
    ident.update({"repo_head": subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
                  "harness_sha256": sha(EVAL / "harness70.py"), "assess_sha256": sha(EVAL / "assess70.py"), "core_sha256": sha(EVAL / "core70.py"),
                  "assessment_evidence_sha256": sha(EVAL / "assessment_evidence.py"),
                  "builder_sha256": sha(HERE / "build_campaign_record.py"), "h4_sha256": sha(HERE / "h4.py"),
                  "prepare_campaign_sha256": sha(Path(__file__).resolve()), "campaign_run_sha256": sha(HERE / "campaign_run.py"),
                  "campaign_assess_sha256": sha(HERE / "campaign_assess.py"),
                  "campaign_cb_sha256": sha(HERE / "campaign_cb.py")})
    write_json(path, ident)
    print(json.dumps({k: ident[k] for k in ("repo_head", "builder_sha256", "h4_sha256", "prepare_campaign_sha256", "refreshes")}, indent=1))
    return 0


def cmd_freeze_evaluator(a) -> int:
    """Freeze the evaluator profile in an existing campaign directory and record it in campaign-identity.json."""
    keys = a.work / "keys"
    if (keys / "omp-evaluator-readonly.json").exists():
        sys.exit("the evaluator profile is already frozen here; a different model is a new campaign identity")
    build_evaluator_key(a.work, a.model)
    bundle = core70.load_profile(keys / "omp-evaluator-readonly.json", keys / "omp-evaluator-readonly.capabilities.json")
    errors = (core70.profile_claim_errors(bundle, []) + omp_eval.eval_profile_errors(bundle.profile)
              + omp.runtime_dependency_errors(bundle.profile))
    if errors:
        (keys / "omp-evaluator-readonly.json").unlink()
        (keys / "omp-evaluator-readonly.capabilities.json").unlink()
        sys.exit(f"evaluator profile refused: {errors}")
    path = a.work / "campaign-identity.json"
    ident = json.loads(path.read_text())
    ident["evaluator_profile"] = "frozen"
    ident["evaluator_agent_model"] = bundle.profile["agent_model"]
    ident["evaluator_profile_sha256"] = sha(keys / "omp-evaluator-readonly.json")
    ident["evaluator_profile_key_sha256"] = bundle.profile_key_sha256
    ident["evaluator_budgets"] = bundle.profile["budgets"]
    ident["evaluator_credential_env"] = bundle.profile["containment_policy"]["provider_route"]["credential_env"]
    write_json(path, ident)
    print(json.dumps({k: ident[k] for k in ident if k.startswith("evaluator")}, indent=1))
    return 0


def row(ok: bool, name: str, detail: str = "") -> bool:
    print(f"{'OK  ' if ok else 'STOP'} {name}{(': ' + detail) if detail else ''}")
    return ok


def cmd_preflight(a) -> int:
    """Every check an operator would otherwise do by eye. Prints OK or STOP per line; exit 0 only if nothing STOPs."""
    import os
    import shutil
    work, ok = a.work, True
    ident = json.loads((work / "campaign-identity.json").read_text())
    ready = (work / "READY")
    tokens = {"launch": "OPERATOR MAY LAUNCH", "evaluation": "EVALUATION MAY START", "calibration": "CALIBRATION MAY START"}
    text = ready.read_text() if ready.exists() else ""
    ok &= row(tokens[a.phase] in text, f"READY says {tokens[a.phase]!r}", "" if tokens[a.phase] in text else "the READY file is missing or does not say it")
    try:
        arms, _ = load_arms(work)
        bad = [n for n, r in arms.items() if harness70.resolve_arm_dist(r) and r["dist_tree_sha256"] != ident["arms"][n]["dist_tree_sha256"]]
        ok &= row(not bad, "arm packages match the recorded identities", ",".join(bad))
    except Exception as exc:  # noqa: BLE001
        ok &= row(False, "arm packages", str(exc))
    keys = work / "keys"
    ok &= row(sha(keys / "omp-primary-flash-executor-main.json") == ident["executor_profile_sha256"], "executor profile digest matches")
    ev = keys / "omp-evaluator-readonly.json"
    ok &= row(ev.exists() and sha(ev) == ident.get("evaluator_profile_sha256"), "evaluator profile is frozen and matches",
              ident.get("evaluator_agent_model", "not frozen"))
    try:
        evaluator = core70.load_profile(ev, keys / "omp-evaluator-readonly.capabilities.json")
        errors = (core70.profile_claim_errors(evaluator, []) + omp_eval.eval_profile_errors(evaluator.profile)
                  + omp.runtime_dependency_errors(evaluator.profile))
        if evaluator.profile_key_sha256 != ident.get("evaluator_profile_key_sha256"):
            errors.append("evaluator profile key differs from the recorded identity")
        if evaluator.profile["agent_model"] == executor(work).profile["agent_model"]:
            errors.append("evaluator model must not be the executor model")
        ok &= row(not errors, "evaluator profile is admissible for omp_eval", "; ".join(errors))
    except (core70.ContractError, OSError, ValueError) as exc:
        ok &= row(False, "evaluator profile is admissible for omp_eval", str(exc))
    for name, path, key in (("builder", HERE / "build_campaign_record.py", "builder_sha256"), ("h4", HERE / "h4.py", "h4_sha256"),
                            ("prepare_campaign", Path(__file__).resolve(), "prepare_campaign_sha256"),
                            ("campaign_run", HERE / "campaign_run.py", "campaign_run_sha256"),
                            ("campaign_assess", HERE / "campaign_assess.py", "campaign_assess_sha256"),
                            ("campaign_cb", HERE / "campaign_cb.py", "campaign_cb_sha256"),
                            ("harness70", EVAL / "harness70.py", "harness_sha256"), ("assess70", EVAL / "assess70.py", "assess_sha256"),
                            ("core70", EVAL / "core70.py", "core_sha256"),
                            ("assessment_evidence", EVAL / "assessment_evidence.py", "assessment_evidence_sha256")):
        ok &= row(sha(path) == ident.get(key), f"tool unchanged since the identity record: {name}")
    drift = subprocess.run(["git", "-C", str(REPO), "diff", "--stat", ident["candidate_ref"], "HEAD", "--", "source", "dist"], capture_output=True, text=True).stdout.strip()
    ok &= row(not drift, "candidate source and dist unchanged from the frozen identity")
    p = subprocess.run([sys.executable, str(Path(__file__).resolve()), "check-plan", "--work", str(work)], capture_output=True, text=True)
    ok &= row(p.returncode == 0 and '"PASS"' in p.stdout, "check-plan passes", "" if p.returncode == 0 else p.stdout[-300:])
    st = json.loads((work / "static-premeasurement.json").read_text())["verdict"]
    ok &= row(st == "PASS", "static pre-measurement", st)
    omp_bin = Path.home() / ".local/bin/omp"
    prof = json.loads((keys / "omp-primary-flash-executor-main.json").read_text())
    ok &= row(omp_bin.is_file() and sha(omp_bin) == prof["provider_runtime"]["executable_sha256"], "omp binary matches the profile digest")
    ok &= row(Path("/usr/bin/bwrap").exists(), "bubblewrap present")
    free = shutil.disk_usage(work).free / 1e9
    ok &= row(free >= 60, "free disk space", f"{free:.0f} GB free (the campaign needs about 25 GB; 60 required)")
    if a.custody and a.phase != "calibration":
        gate = json.loads((a.custody / "FREEZE-GATE.json").read_text())
        want = {"candidate_frozen": True, "frozen_run_output_exists": False} if a.phase == "launch" and not (work / "runs").exists() else None
        ok &= row(want is None or gate == want, "custody FREEZE-GATE", json.dumps(gate))
    if a.need_credential:
        ok &= row(bool(os.environ.get("SSDP70_OMP_PROVIDER_CREDENTIAL")), "SSDP70_OMP_PROVIDER_CREDENTIAL is set in this shell (value not shown)")
    ok &= row(not (work / "launch" / "HALT").exists(), "no HALT file in launch/")
    print("RESULT:", "ALL OK" if ok else "STOP: write an escalation packet; do not continue")
    return 0 if ok else 2


def cmd_assemble(a) -> int:
    """Merge the built record with Precondition C inputs and the static block into the final `h4.py score` input."""
    rec = json.loads(a.record.read_text())
    ca = json.loads(a.c_a.read_text())
    cb = json.loads(a.c_b.read_text())
    need = ("n", "agree", "failures", "caught")
    if any(k not in cb for k in need):
        sys.exit(f"the C(b) counts lack one of {need}; use the custodian's score_cb.py output")
    if not all(isinstance(o.get("good_ok"), bool) and isinstance(o.get("bad_ok"), bool) for o in ca.get("oracles", [])):
        sys.exit("the C(a) record is malformed")
    static = json.loads(a.static.read_text())
    rec["precondition"] = {"oracles": ca["oracles"], "evaluator": {k: cb[k] for k in need}, "attempt": a.attempt}
    q5d = static.get("q5d", {}).get("passed", False)
    rec["static"] = {"byte_identical": q5d, "mapping_complete": q5d, "block_bytes": a.block_bytes}
    rec.setdefault("descriptive", {})["q5c_static_premeasurement"] = static["verdict"]
    a.out.write_text(json.dumps(rec, indent=1) + "\n")
    print(json.dumps({"out": str(a.out), "oracles": len(ca["oracles"]), "evaluator": rec["precondition"]["evaluator"], "attempt": a.attempt}))
    return 0


def cmd_report(a) -> int:
    """One file the operator sends back: status, verification, costs, escalations, identity."""
    work = a.work
    run = lambda *args: subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True).stdout  # noqa: E731
    parts = ["# Operator report", "", "## Run status", "```", run(HERE / "campaign_run.py", work, "status"), "```"]
    ident = json.loads((work / "campaign-identity.json").read_text())
    parts += ["## Identity", "```", json.dumps({k: ident[k] for k in ("candidate_ref", "executor_agent_model", "evaluator_agent_model", "repo_head") if k in ident}, indent=1), "```"]
    for f in ("campaign-verify.json", "dispositions.json"):
        if (work / f).exists():
            parts += [f"## {f} (head)", "```", (work / f).read_text()[:3000], "```"]
    esc = sorted((work / "escalations").glob("*")) if (work / "escalations").exists() else []
    parts += ["## Escalation packets", *([f"- {e.name}" for e in esc] or ["- none"])]
    auth = sorted((work / "authorizations").glob("*")) if (work / "authorizations").exists() else []
    parts += ["## Authorizations present", *([f"- {e.name}" for e in auth] or ["- none"])]
    parts += ["## Run directories", *[f"- {d.name}: {len(list(d.glob('*-r*/summary.json')))} summaries" for d in sorted((work / "runs").glob("*")) if d.is_dir()]]
    out = work / "OPERATOR-REPORT.md"
    out.write_text("\n".join(parts) + "\n")
    print(f"wrote {out}")
    return 0


def cmd_static(a) -> int:
    arms, _ = load_arms(a.work)
    dist = harness70.resolve_arm_dist(arms["p72"])
    root = dist / "software-implementation"
    entry = (root / "SKILL.md").stat().st_size
    workflow = (root / "references" / "workflow-and-workplans.md").stat().st_size
    inspect_owner = (root / "references" / "scientific-inspectability-and-initiative.md").stat().st_size
    rows = []
    for route, mode, candidate, base in (("T1/T8", "entrypoint-only", entry, STATIC_BASELINES["entry"]),
                                         ("T7", "entrypoint-only", entry, STATIC_BASELINES["entry"]),
                                         ("T7", "workflow-owner", entry + workflow, STATIC_BASELINES["owner"])):
        limit = 2 * base - MARGIN
        rows.append({"route": route, "mode": mode, "candidate_bytes": candidate, "cap": 2 * base, "limit_with_margin": limit,
                     "headroom": limit - candidate, "verdict": "OK" if candidate <= limit else "BREACH"})
    risks = [{"case": "T1/T8 run that also reads the scientific-inspectability owner", "bytes": entry + inspect_owner,
              "limit": 2 * STATIC_BASELINES["entry"] - MARGIN}]
    out = {"schema": 1, "baselines": "historical 6.5 planning figures (Q5C-STATIC-PREMEASUREMENT-2026-10-07.md); live Q5c uses fresh paired 6.5 runs",
           "sizes": {"entrypoint": entry, "workflow_owner": workflow, "scientific_inspectability_owner": inspect_owner},
           "rows": rows, "outside_enumerated_modes": risks,
           "verdict": "PASS" if all(r["verdict"] == "OK" for r in rows) else "BREACH: stops qualification, goes to the stakeholder (contract section 5)"}
    t = subprocess.run([sys.executable, "-m", "unittest", "tests.test_protocol_72_scientific_checks"], cwd=REPO, capture_output=True, text=True)
    out["q5d"] = {"tests": "tests.test_protocol_72_scientific_checks", "passed": t.returncode == 0, "tail": t.stderr.strip().splitlines()[-3:],
                  "covers": "O-2 byte identity of the 6.6 text outside the block (source and dist), frozen-minimum mapping complete"}
    if t.returncode != 0:
        out["verdict"] = "BREACH: the Q5d static tests fail (" + out["verdict"] + ")"
    write_json(a.work / "static-premeasurement.json", out)
    print(json.dumps(out, indent=1))
    return 0 if out["verdict"] == "PASS" else 2


def read_flags(path: Path | None) -> dict:
    return json.loads(path.read_text()) if path else {}


def corpus_rows(corpus: Path):
    return harness70.load_manifest(corpus)


def panel_arms(panel: str, config: dict) -> list[str] | None:
    table = {**PANEL_ARMS, **config.get("panel_arms", {})}
    base = panel[:-4] if panel.endswith("-add") else panel
    return table.get(base)


def cmd_check_corpus(a) -> int:
    arms, _ = load_arms(a.work)
    bundle = executor(a.work)
    config = json.loads(a.config.read_text()) if a.config else {}
    flags = read_flags(a.slot_flags)
    dists = {n: harness70.resolve_arm_dist(r) for n, r in arms.items()}
    problems, counts = [], {}
    episodes = corpus_rows(a.corpus)
    for e in episodes:
        i, panel = e["id"], e.get("panel")
        used = panel_arms(panel, config) if panel else None
        if used is None:
            problems.append(f"{i}: unknown or missing panel {panel!r}")
            continue
        counts.setdefault(panel, [0, 0])
        counts[panel][0] += 1
        counts[panel][1] += int(e.get("replicates", 1))
        if harness70.entry_stratum(e, bundle.profile) != "deterministic":
            problems.append(f"{i}: entry does not resolve deterministic")
        root = e.get("entry", "").split(":", 1)[-1]
        for arm in used:
            if not (dists[arm] / root / "SKILL.md").is_file():
                problems.append(f"{i}: root {root!r} absent from {arm}")
        if int(e.get("max_turns", 0)) != 60:
            problems.append(f"{i}: max_turns {e.get('max_turns')!r} is not the panel cap 60")
        try:
            core70.load_requirements(a.requirements, i)
        except core70.ContractError as exc:
            problems.append(f"{i}: requirements: {exc}")
        if not (a.oracles / i).is_dir():
            problems.append(f"{i}: oracle directory missing")
        if panel == "main":
            f = flags.get(i)
            if f is None or any(k not in f for k in ("delegate", "non_owed", "scored")):
                problems.append(f"{i}: main-panel episode lacks the delegate/non_owed/scored slot flags")
    main = [e for e in episodes if e.get("panel") == "main"]
    summary = {"episodes": len(episodes), "by_panel(episodes,runs_per_arm)": counts,
               "main_delegate": sum(bool(flags.get(e["id"], {}).get("delegate")) for e in main),
               "main_non_owed": sum(bool(flags.get(e["id"], {}).get("non_owed")) for e in main)}
    print(json.dumps({"verdict": "PASS" if not problems else "FAIL", "problems": problems, "summary": summary}, indent=1))
    return 0 if not problems else 2


def cmd_plan(a) -> int:
    work = a.work
    if (work / "commands.json").exists():
        sys.exit(f"refusing to overwrite {work / 'commands.json'}")
    config = json.loads(a.config.read_text()) if a.config else {}
    flags = read_flags(a.slot_flags)
    bundle = executor(work)
    episodes = corpus_rows(a.corpus)
    arms_path = work / "arms" / "arms.json"
    common = ["/usr/bin/python3", str(EVAL / "harness70.py"), "matrix", "--arms-manifest", str(arms_path),
              "--profile", str(work / "keys" / "omp-primary-flash-executor-main.json"),
              "--capabilities", str(work / "keys" / "omp-primary-flash-executor-main.capabilities.json"),
              "--adapter", "omp", "--mode", "qualification"]
    parallel = min(int(config.get("parallel", PARALLEL_MAX)), PARALLEL_MAX)
    chunk = int(config.get("chunk", CHUNK))
    cond_chunk = int(config.get("conditional_chunk", 2))      # add-ons run two episodes at a time (the T7 rule adds two pairs, then re-checks)
    by_panel: dict[str, list[dict]] = {}
    for e in episodes:
        by_panel.setdefault(e["panel"], []).append(e)
    order = [p for p in ("main", "routing", "versioning", "burden", "sentinels", "unversioned", "r2", "ordinary") if p in by_panel]
    order += sorted(p for p in by_panel if p not in order and not p.endswith("-add"))
    order += sorted(p for p in by_panel if p.endswith("-add"))
    commands, slots, cond_slots = [], [], []
    for panel in order:
        used = panel_arms(panel, config)
        conditional = panel.endswith("-add")
        rows = by_panel[panel]
        size = cond_chunk if conditional else chunk
        for n in range(0, len(rows), size):
            part = rows[n:n + size]
            key = f"{panel}-c{n // size + 1:02d}"
            argv = [*common, "--corpus", str(a.corpus), "--out", str(work / "runs" / key), "--requirements", str(a.requirements),
                    "--oracles", str(a.oracles), "--parallel", str(parallel)]
            for arm in used:
                argv += ["--arm", arm]
            for e in part:
                argv += ["--only", e["id"]]
            runs = sum(int(e.get("replicates", 1)) for e in part) * len(used)
            commands.append({"key": key, "panel": panel, "stage": 1 if panel == "main" else 2, "conditional": conditional,
                             "episodes": len(part), "runs": runs,
                             "arms": used, "argv": argv, "shell": shlex.join(argv)})
            for e in part:
                f = flags.get(e["id"], {})
                for arm in used:
                    for rep in range(int(e.get("replicates", 1))):
                        slot = {"episode": e["id"], "arm": LABELS[arm], "replicate": rep, "panel": panel, "command": key}
                        if panel == "main":
                            slot.update({k: bool(f.get(k)) for k in ("delegate", "non_owed", "scored")})
                        else:
                            slot["scored"] = bool(f.get("scored", False))
                        (cond_slots if conditional else slots).append(slot)
    write_json(work / "commands.json", {"schema": 1, "purpose": "qualification", "commands": commands})
    declaration = {"slots": slots, "conditional_slots": cond_slots, "arms": LABELS and {v: k for k, v in LABELS.items()},
                   "q5c_routes": ROUTES, "execution_mode": "qualification", "purpose": "qualification",
                   "profile_key_sha256": bundle.profile_key_sha256, "check_pair_order": True}
    write_json(work / "declaration.json", declaration)
    expected = {c["key"]: {"runs": c["runs"], "conditional": c["conditional"]} for c in commands}
    write_json(work / "expected-runs.json", {"unconditional_runs": sum(c["runs"] for c in commands if not c["conditional"]),
                                              "conditional_runs": sum(c["runs"] for c in commands if c["conditional"]), "commands": expected})
    print(json.dumps({"commands": len(commands), "unconditional_runs": sum(c["runs"] for c in commands if not c["conditional"]),
                      "conditional_runs": sum(c["runs"] for c in commands if c["conditional"]),
                      "slots": len(slots), "conditional_slots": len(cond_slots)}, indent=1))
    return 0


def cmd_check_plan(a) -> int:
    work, problems = a.work, []
    plan = json.loads((work / "commands.json").read_text())["commands"]
    decl = json.loads((work / "declaration.json").read_text())
    arms, _ = load_arms(work)
    bundle = executor(work)
    problems += [f"executor profile: {e}" for e in omp.profile_errors(bundle.profile)]
    if bundle.profile["budgets"] != {"max_turns": 60, "timeout_s": 2400}:
        problems.append(f"executor budgets are {bundle.profile['budgets']}")
    for name in {n for c in plan for n in c["arms"]}:
        try:
            harness70.resolve_arm_dist(arms[name])
        except (KeyError, core70.ContractError) as exc:
            problems.append(f"arm {name}: {exc}")
    seen, total = set(), 0
    for c in plan:
        argv = c["argv"]
        arg = lambda flag: Path(argv[argv.index(flag) + 1])  # noqa: E731
        if int(argv[argv.index("--parallel") + 1]) > PARALLEL_MAX:
            problems.append(f"{c['key']}: parallel above {PARALLEL_MAX}")
        if argv[argv.index("--mode") + 1] != "qualification":
            problems.append(f"{c['key']}: mode is not qualification")
        corpus = {e["id"]: e for e in corpus_rows(arg("--corpus"))}
        for i in [argv[j + 1] for j, x in enumerate(argv) if x == "--only"]:
            if i not in corpus:
                problems.append(f"{c['key']}: {i} missing from the corpus")
                continue
            for arm in c["arms"]:
                for rep in range(int(corpus[i].get("replicates", 1))):
                    s = (i, arm, rep)
                    total += 1
                    if s in seen:
                        problems.append(f"duplicate slot {s}")
                    seen.add(s)
    declared = len(decl["slots"]) + len(decl["conditional_slots"])
    if declared != total:
        problems.append(f"declaration has {declared} slots, the plan {total}")
    print(json.dumps({"verdict": "PASS" if not problems else "FAIL", "problems": problems, "planned_runs": total,
                      "commands": len(plan)}, indent=1))
    return 0 if not problems else 2


def cmd_verify(a) -> int:
    work = a.work
    arms, _ = load_arms(work)
    roots = [d for d in sorted((work / "runs").glob("*")) if d.is_dir() and not d.name.startswith("rerun")]
    reruns = [d for d in sorted((work / "runs").glob("rerun*")) if d.is_dir()]
    if not roots:
        print("no run directories yet under runs/")
        return 2
    decl = json.loads((work / "declaration.json").read_text())
    run_decl = {k: v for k, v in decl.items() if k != "conditional_slots"}
    stage_of = {c["panel"]: int(c.get("stage", 1)) for c in json.loads((work / "commands.json").read_text())["commands"]}
    if a.stage:                                                      # only the stages launched so far are declared
        run_decl["slots"] = [x for x in decl["slots"] if stage_of.get(x["panel"], 1) <= a.stage]
    if a.include_conditional:                                          # only the conditional commands that were authorized and run
        keys = set(a.include_conditional)
        run_decl["slots"] = run_decl["slots"] + [x for x in decl["conditional_slots"] if x.get("command") in keys]
    (work / "declaration.effective.json").write_text(json.dumps(run_decl))
    cmd = [sys.executable, str(HERE / "build_campaign_record.py"), "--declaration", str(work / "declaration.effective.json"),
           "--map", str(a.map), "--allow-unresolved", "--audit", str(work / "campaign-verify.json")]
    for r in roots:
        cmd += ["--runs", str(r)]
    for r in reruns:
        cmd += ["--rerun", str(r)]
    for name, row in arms.items():
        cmd += ["--subject-commit", f"{name}={row['commit']}"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    print(p.stdout)
    sys.stderr.write(p.stderr)
    return p.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("init", "static", "check-corpus", "plan", "check-plan", "verify", "refresh-identity", "freeze-evaluator", "preflight", "report", "assemble"):
        sp = sub.add_parser(name)
        sp.add_argument("--work", type=Path, required=True)
        if name == "init":
            sp.add_argument("--candidate-ref", default=CANDIDATE_REF)
            sp.add_argument("--evaluator-model", help="model id on the deepinfra route (never the executor model); omit to leave the evaluator unfrozen")
        if name == "freeze-evaluator":
            sp.add_argument("--model", required=True, help="model id on the deepinfra route, never the executor model")
        if name == "assemble":
            sp.add_argument("--record", type=Path, required=True)
            sp.add_argument("--c-a", type=Path, required=True)
            sp.add_argument("--c-b", type=Path, required=True)
            sp.add_argument("--static", type=Path, required=True)
            sp.add_argument("--attempt", type=int, default=1)
            sp.add_argument("--block-bytes", type=int, default=0)
            sp.add_argument("--out", type=Path, required=True)
        if name == "preflight":
            sp.add_argument("--phase", choices=("launch", "evaluation", "calibration"), required=True)
            sp.add_argument("--custody", type=Path)
            sp.add_argument("--need-credential", action="store_true")
        if name in ("check-corpus", "plan"):
            sp.add_argument("--corpus", type=Path, required=True)
            sp.add_argument("--requirements", type=Path, required=True)
            sp.add_argument("--oracles", type=Path, required=True)
            sp.add_argument("--slot-flags", type=Path)
            sp.add_argument("--config", type=Path)
        if name == "verify":
            sp.add_argument("--map", type=Path, required=True)
            sp.add_argument("--include-conditional", nargs="+", metavar="KEY", help="conditional command keys that were authorized and run")
            sp.add_argument("--stage", type=int, help="verify only the slots of stages up to N (default: all unconditional slots)")
    a = ap.parse_args()
    return {"init": cmd_init, "static": cmd_static, "check-corpus": cmd_check_corpus, "plan": cmd_plan,
            "check-plan": cmd_check_plan, "verify": cmd_verify, "refresh-identity": cmd_refresh_identity,
            "freeze-evaluator": cmd_freeze_evaluator, "preflight": cmd_preflight, "report": cmd_report, "assemble": cmd_assemble}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
