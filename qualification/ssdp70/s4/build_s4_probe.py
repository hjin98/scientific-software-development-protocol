#!/usr/bin/env python3
"""Analyst tool: build and statically check the S4 development-probe inputs (pre-registration S4-DEVELOPMENT-PROBE-PREREGISTRATION).

Writes, under --work: the arms manifest for the frozen 7.2.0 candidate (p72), the re-frozen 60-turn / 2400 s executor key,
the burden-route overlay (T1/T7/T8 from the disclosed 6.6 fixtures, with trivial requirements: the probe measures bytes and
owner reads on these, not correctness), and commands.json (two harness matrix commands, one arm each, so all runs are
independent). `--check` runs the provider-free pre-check. Development purpose only. Opens no custodian key.
"""
from __future__ import annotations

import argparse
import json
import shlex
import shutil
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EVAL = REPO / "qualification" / "ssdp70" / "eval"
sys.path.insert(0, str(EVAL))
import core70  # noqa: E402
import harness70  # noqa: E402
import prepare_arms70  # noqa: E402
from adapters import omp  # noqa: E402

FIXTURES66 = REPO / "qualification" / "ssdp66" / "eval" / "fixtures"
ROUTES = {"T1": "T1-first-clean-local-repair", "T8": "T8-ordinary-feature-with-docs", "T7": "T7-unversioned-workplan-implementation"}
ROOT = "software-implementation"
CORPUS_A = Path.home() / "ssdp70-omp-stagef/qualification/requal71-20261006/dev/corpus"     # the 7.1 development overlay (92 episodes)
CUSTODY_REQ = Path.home() / "ssdp70-fixture-custody/requirements"
CUSTODY_ORACLES = Path.home() / "ssdp70-fixture-custody/oracles"
ARTIFACTS = ["summary.json", "run-identity.json", "trace.jsonl", "events.normalized.jsonl", "normalization-map.json", "final-report.md",
             "final-tree", "oracle.json", "requirements-snapshot.json", "adapter-artifacts", "project-control-record.json"]


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_key(work: Path) -> tuple[Path, Path]:
    """Re-freeze the executor profile from the adapter template (the committed profile pins retired modules) and derive the main key."""
    template = json.loads((EVAL / "profiles" / "omp-headless.template.json").read_text())
    source = json.loads((EVAL / "profiles" / "omp-primary-flash-executor.json").read_text())
    route = {k: v for k, v in source["containment_policy"]["provider_route"].items()}
    profile = omp.freeze_profile(template, executable_path=str(Path.home() / ".local/bin/omp"), provider_route=route,
                                 reasoning=source["reasoning_configuration"], profile_id="omp-primary-flash-executor-main",
                                 budgets={"max_turns": 60, "timeout_s": 2400})
    profile["activation_mechanism"] = "runtime-command"
    profile["runtime_input_template"] = omp.input_template("runtime-command")
    errors = omp.profile_errors(profile)
    if errors:
        sys.exit(f"re-frozen profile is not admissible: {errors}")
    keys = work / "keys"
    out_profile, out_caps = keys / "omp-primary-flash-executor-main.json", keys / "omp-primary-flash-executor-main.capabilities.json"
    write_json(out_profile, profile)
    shutil.copy2(EVAL / "capabilities" / "omp-headless.json", out_caps)
    return out_profile, out_caps


def build_routes(work: Path, counts: dict[str, int]) -> list[str]:
    """Overlay corpus, trivial requirements and oracles for the burden routes."""
    corpus, req, oracles = work / "routes" / "corpus", work / "routes" / "requirements", work / "routes" / "oracles"
    episodes = []
    for route, n in counts.items():
        fixture = FIXTURES66 / ROUTES[route]
        target = corpus / "fixtures" / ROUTES[route] / "project"
        if not target.exists():
            shutil.copytree(fixture, target, ignore=shutil.ignore_patterns("__pycache__"))
        prompt = (fixture / "TASK.md").read_text(encoding="utf-8").strip()
        for i in range(1, n + 1):
            episodes.append({"id": f"{route}-r{i:02d}", "fixture": ROUTES[route], "prompt": prompt, "entry": f"pinned:{ROOT}",
                             "max_turns": 60, "replicates": 1, "panel": "main", "claims": [], "account": "assistant"})
    corpus.mkdir(parents=True, exist_ok=True)
    (corpus / "manifest.yaml").write_text(yaml.safe_dump({"schema": "ssdp70-corpus-manifest/1", "episodes": episodes}), encoding="utf-8")
    ids = [e["id"] for e in episodes]
    write_json(req / "required_artifacts.json", {"schema": 1, "episodes": {i: ARTIFACTS for i in ids}})
    write_json(req / "required_oracles.json", {"schema": 1, "episodes": {i: [{"id": "o1", "path": "check_o1.py"}] for i in ids}})
    write_json(req / "expected_scoring_items.json", {"schema": 1, "episodes": {i: [
        {"id": "i1", "measure": "burden-route", "critical": False, "branch": "main", "allowed_dispositions": ["pass", "fail", "unresolved"]}] for i in ids}})
    for i in ids:
        (oracles / i).mkdir(parents=True, exist_ok=True)
        (oracles / i / "check_o1.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    return ids


def build(a: argparse.Namespace) -> int:
    work = a.work
    if (work / "commands.json").exists():
        sys.exit(f"refusing to overwrite {work}")
    arms = work / "arms"
    record = prepare_arms70.extract_arm(REPO, arms, "p72", a.candidate_ref, "7.2.0")
    write_json(arms / "arms.json", {"schema": 1, "repo": str(REPO), "arms": [record]})
    profile, caps = build_key(work)
    counts = {"T1": a.t1, "T8": a.t8, "T7": a.t7}
    route_ids = build_routes(work, counts)
    manifest = yaml.safe_load((CORPUS_A / "manifest.yaml").read_text())["episodes"]
    ids_a = [e["id"] for e in manifest]
    out_root = work / "runs"
    if not any(r.resolve() in out_root.resolve().parents for r in omp.RUN_REALIZATION_ROOTS):
        sys.exit(f"{out_root} is not beneath an approved OMP realization root")
    common = ["/usr/bin/python3", str(EVAL / "harness70.py"), "matrix", "--arms-manifest", str(arms / "arms.json"), "--arm", "p72",
              "--profile", str(profile), "--capabilities", str(caps), "--adapter", "omp", "--mode", "probe"]
    commands = []
    for key, corpus, requirements, oracles, ids, parallel in (
            ("s4-a", CORPUS_A, CUSTODY_REQ, CUSTODY_ORACLES, ids_a, a.parallel_a),
            ("s4-routes", work / "routes" / "corpus", work / "routes" / "requirements", work / "routes" / "oracles", route_ids, a.parallel_routes)):
        argv = [*common, "--corpus", str(corpus), "--out", str(out_root / key), "--requirements", str(requirements),
                "--oracles", str(oracles), "--parallel", str(parallel)]
        for i in ids:
            argv += ["--only", i]
        commands.append({"key": key, "episodes": len(ids), "runs": len(ids), "argv": argv, "shell": shlex.join(argv)})
    write_json(work / "commands.json", {"schema": 1, "purpose": "development", "commands": commands})
    print(json.dumps({"arm": {k: record[k] for k in ("name", "commit", "version", "dist_tree_sha256")},
                      "commands": {c["key"]: c["runs"] for c in commands}, "total_runs": sum(c["runs"] for c in commands)}, indent=1))
    return 0


def check(a: argparse.Namespace) -> int:
    """Provider-free pre-check: everything the harness will resolve before launching a subject."""
    work, problems = a.work, []
    commands = json.loads((work / "commands.json").read_text())["commands"]
    arms, _ = harness70.load_arms_manifest(work / "arms" / "arms.json")
    arm = arms["p72"]
    dist = harness70.resolve_arm_dist(arm)
    if core70.sha256_tree(dist) != arm["dist_tree_sha256"]:
        problems.append("p72 package digest differs from the arms manifest")
    for skill in prepare_arms70.SKILLS:
        if not (dist / skill / "SKILL.md").is_file():
            problems.append(f"p72 package lacks {skill}")
    for cmd in commands:
        argv = cmd["argv"]
        arg = lambda flag: Path(argv[argv.index(flag) + 1])  # noqa: E731
        bundle = core70.load_profile(arg("--profile"), arg("--capabilities"))
        problems += [f"{cmd['key']} profile: {e}" for e in omp.profile_errors(bundle.profile)]
        only = [argv[i + 1] for i, x in enumerate(argv) if x == "--only"]
        episodes = {e["id"]: e for e in harness70.load_manifest(arg("--corpus"))}
        for ident in only:
            episode = episodes.get(ident)
            if episode is None:
                problems.append(f"{cmd['key']}: {ident} missing from the corpus")
                continue
            root = episode["entry"].split(":", 1)[-1]
            if harness70.entry_stratum(episode, bundle.profile) != "deterministic":
                problems.append(f"{ident}: entry does not resolve deterministic")
            if not (dist / root / "SKILL.md").is_file():
                problems.append(f"{ident}: root {root} is absent from p72")
            try:
                core70.load_requirements(arg("--requirements"), ident)
            except core70.ContractError as exc:
                problems.append(f"{ident}: requirements: {exc}")
            if not (arg("--oracles") / ident).is_dir():
                problems.append(f"{ident}: oracle directory missing")
    print(json.dumps({"verdict": "PASS" if not problems else "FAIL", "problems": problems, "commands": {c["key"]: c["runs"] for c in commands}}, indent=1))
    return 0 if not problems else 2


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=("build", "check"))
    ap.add_argument("--work", type=Path, default=Path.home() / "ssdp70-omp-stagef/qualification/s4-20261007")
    ap.add_argument("--candidate-ref", default="2dedcfa3408f62bc11a696ac3776183a87b40438")
    ap.add_argument("--t1", type=int, default=15)
    ap.add_argument("--t8", type=int, default=15)
    ap.add_argument("--t7", type=int, default=7)
    ap.add_argument("--parallel-a", type=int, default=20)
    ap.add_argument("--parallel-routes", type=int, default=8)
    a = ap.parse_args()
    return build(a) if a.command == "build" else check(a)


if __name__ == "__main__":
    raise SystemExit(main())
