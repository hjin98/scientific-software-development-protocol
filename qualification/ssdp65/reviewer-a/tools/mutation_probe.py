#!/usr/bin/env python3
"""Oracle-strength probe for the frozen Protocol 6.4 acceptance workflow (P0).

Diagnostic evidence only; not a protocol validator and not authority.

For each mutant, the probe creates a disposable Git worktree at the requested
baseline commit, applies one exact textual mutation to canonical `source/`,
regenerates the committed descendants exactly as a legitimate source change
would (`dist/` via `source/build_skills.py`, the current Orchestrator snapshot
via `orchestrator/scripts/generate_protocol_snapshot.py`), and then runs the
documented repository acceptance workflow.  A mutant is DETECTED when at least
one acceptance step fails.

Mutants are of two kinds:

* SEMANTIC  - inverts or deletes a governing doctrine while leaving any phrase
              that the suite might assert elsewhere untouched.  A robust
              acceptance workflow for a document-controlled protocol should be
              expected to reject most of these.
* PARAPHRASE - a meaning-preserving rewording.  A discriminating oracle should
              accept these; detection here is a false positive.
* CONTROL   - deletes a phrase the suite is known to assert.  These validate
              that the harness itself can observe a failing acceptance run.

Usage:
    python mutation_probe.py --repo <repo> --base <commit> --work <scratch-dir> \
        --python <python-with-deps> [--only M01,M02] [--skip-core]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

K = "source/shared/references/abstraction-and-concretization.md"
EV = "source/shared/references/evidence-evolution-and-dependencies.md"
D1 = "source/shared/references/scientific-formulation.md"
D2 = "source/shared/references/numerical-algorithm-design.md"
D4 = "source/shared/references/specification-and-implementation.md"
TV = "source/shared/references/testing-and-validation.md"
WF = "source/shared/references/workflow-and-workplans.md"
PR = "source/shared/references/development-workflow-prompts.md"
IMPL = "source/roles/software-implementation/SKILL.md"
PEM = "source/shared/references/project-engineering-memory.md"


@dataclass(frozen=True)
class Mutant:
    mid: str
    kind: str
    path: str
    old: str
    new: str
    doctrine: str


MUTANTS = [
    Mutant("M01", "SEMANTIC", K,
           "Materially conflicting applicable authorities are not silently prioritized: expose the conflict and route adjudication.",
           "Materially conflicting applicable authorities are resolved by preferring the most recently accepted statement.",
           "owner-conflict adjudication (QF64-B family)"),
    Mutant("M02", "SEMANTIC", EV,
           "A stale passing observation is not admissible confirmation.",
           "A stale passing observation remains admissible confirmation until a newer failure is observed.",
           "stale-pass inadmissibility (evidence core rule)"),
    Mutant("M03", "SEMANTIC", K,
           "Preserve the challenged authority as the explicit baseline rather than silently editing it to fit downstream behavior.",
           "When implementation evidence is strong, edit the challenged authority to fit downstream behavior.",
           "Serious Challenge baseline preservation"),
    Mutant("M04", "SEMANTIC", D4,
           "Never rewrite the specification merely to make unintended code pass.",
           "When code and tests agree, rewrite the specification to match the code.",
           "specification-over-code authority direction (D4)"),
    Mutant("M05", "SEMANTIC", D2,
           "Do not widen tolerances, lower resolution, change estimand/estimator, alter reduction semantics or relax convergence merely because an implementation/backend otherwise fails.",
           "Widen tolerances or relax convergence to the observed backend discrepancy when an implementation/backend otherwise fails.",
           "tolerance ownership (D2)"),
    Mutant("M06", "SEMANTIC", K,
           "Evidence/quantitative claims bind to the material parameter/regime identity actually exercised.",
           "Evidence for any one instance of a parameterized family establishes the claim for the whole family.",
           "parameter-sensitive evidence applicability (QF64-F family)"),
    Mutant("M07", "SEMANTIC", K,
           "For actual runtime context `C`, `context_available_C(x)` additionally requires the exact canonical meaning needed for the current inference to have been supplied/loaded in that context.",
           "For actual runtime context `C`, `context_available_C(x)` holds whenever a route to the owner of `x` is discoverable, even if its meaning was never loaded.",
           "source vs runtime-context availability (QF64-M family)"),
    Mutant("M08", "SEMANTIC", D1,
           "Agents may research/derive/check/design evidence/draft proposals but may not self-accept a designated human-gated change.",
           "Agents may self-accept a designated human-gated change once automated qualification passes.",
           "human ratification gate (D1)"),
    Mutant("M09", "SEMANTIC", IMPL,
           "Test doubles may control dependencies below/outside the owner, but cannot replace the owner whose behavior constitutes the claim.",
           "Test doubles may replace the owner whose behavior constitutes the claim when real-owner integration is expensive.",
           "proxy-proof real-owner acceptance (D4 role)"),
    Mutant("M10", "SEMANTIC", K,
           "Frequency, memory temperature, maturity, qualification, documentation, or historical survival cannot mint an invariant.",
           "A HOT memory family with PROVEN maturity is binding on D3/D4 concretization.",
           "PEM non-authority (no D5)"),
    Mutant("M11", "SEMANTIC", TV,
           "Tolerance derives from accepted D2 error/equivalence semantics, never from the backend result that happened to fail.",
           "Tolerance may be set from the backend result that happened to fail when no reference is available.",
           "tolerance derivation (testing owner)"),
    Mutant("M12", "SEMANTIC", PR,
           "descendants must not reset it to accepted-current or emit an unqualified Pass/complete result while the governing challenge remains unresolved.",
           "descendants may reset it to accepted-current once their own local checks pass.",
           "risk-accepted provisional propagation (orchestration prompt)"),
    Mutant("M13", "SEMANTIC", K,
           "A child can perfectly satisfy a too-weak abstraction and still be wrong; that is an upstream abstraction defect.",
           "A child that satisfies its parent abstraction is correct by construction.",
           "abstraction adequacy (kernel)"),
    Mutant("M14", "SEMANTIC", PEM,
           "Missing, malformed, unsupported, or partial PEM cannot prove no relevant lesson exists.",
           "Missing or partial PEM establishes that no relevant lesson exists.",
           "absence-is-not-evidence (PEM)"),
    Mutant("M15", "SEMANTIC", WF,
           "Missing required pre-Review acceptance remains a blocker; Review does not move those checks later.",
           "Missing required pre-Review acceptance may be deferred until after Review.",
           "Review readiness (workflow)"),
    Mutant("L01", "PARAPHRASE", K,
           "Each material normative claim has one current semantic owner,",
           "Each material normative claim has a single current semantic owner,",
           "lossless paraphrase of unique-ownership sentence"),
    Mutant("L02", "PARAPHRASE", EV,
           "The semantic dependency graph widens impact discovery; it does not recursively warrant endpoints.",
           "The semantic dependency graph broadens impact discovery; it does not recursively warrant endpoints.",
           "lossless paraphrase of dependency-graph warrant sentence"),
    Mutant("L03", "PARAPHRASE", PR,
           "Stored `USES_DEFINITION` direction is `subject -> prerequisite`;",
           "The stored direction of `USES_DEFINITION` is `subject -> prerequisite`;",
           "lossless paraphrase of stored-direction sentence"),
    # C01 originally replaced "`source_available_D(x)`" with "`available(x)`".  That control
    # was invalid: the asserted token also occurs in the kernel's code block, so the pinned
    # phrase survived and the run could not fail.  Replaced before results were frozen.
    Mutant("C01", "CONTROL", K,
           "This is not a closed ontology",
           "This is a closed ontology",
           "control: asserted phrase inverted"),
    Mutant("C02", "CONTROL", PR,
           "CURRENT_PROTOCOL = 6.4.0",
           "CURRENT_PROTOCOL = 6.3.0",
           "control: asserted current-version identity changed"),
]


def run(cmd: list[str], cwd: Path, timeout: int = 900) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return proc.returncode, (proc.stdout + proc.stderr)[-2000:]


def probe(repo: Path, base: str, work: Path, py: str, mutant: Mutant, skip_core: bool) -> dict:
    tree = work / f"wt-{mutant.mid}"
    if tree.exists():
        subprocess.run(["git", "worktree", "remove", "--force", str(tree)], cwd=repo, capture_output=True)
        shutil.rmtree(tree, ignore_errors=True)
    subprocess.run(["git", "worktree", "add", "--detach", str(tree), base], cwd=repo, check=True, capture_output=True)
    result: dict = {"mutant": mutant.mid, "kind": mutant.kind, "path": mutant.path, "doctrine": mutant.doctrine, "steps": {}}
    try:
        target = tree / mutant.path
        text = target.read_text(encoding="utf-8")
        count = text.count(mutant.old)
        if count != 1:
            result["error"] = f"expected exactly one match, found {count}"
            return result
        target.write_text(text.replace(mutant.old, mutant.new), encoding="utf-8")
        # Regenerate committed descendants as a legitimate canonical-source change would.
        rc, out = run([py, "source/build_skills.py", "--output", "dist"], tree)
        result["steps"]["regenerate_dist"] = rc
        rc, out = run([py, "orchestrator/scripts/generate_protocol_snapshot.py"], tree)
        result["steps"]["regenerate_snapshot"] = rc
        scratch_dist = work / f"dist-{mutant.mid}"
        shutil.rmtree(scratch_dist, ignore_errors=True)
        checks = [
            ("unittest", [py, "-m", "unittest", "discover", "-s", "tests"]),
            ("pem_validate", [py, "source/project_engineering_memory.py", "PROJECT-ENGINEERING-MEMORY.md"]),
            ("build", [py, "source/build_skills.py", "--output", str(scratch_dist)]),
            ("validate_packages", [py, "source/validate_packages.py", "--dist", str(scratch_dist)]),
            ("check_dist", [py, "source/check_dist.py", "--expected", str(scratch_dist), "--committed", "dist"]),
            ("snapshot_check", [py, "orchestrator/scripts/generate_protocol_snapshot.py", "--check"]),
        ]
        if not skip_core:
            checks.append(("core_tests", [py, "orchestrator/scripts/run_core_tests.py"]))
        failing: list[str] = []
        for name, cmd in checks:
            rc, out = run(cmd, tree)
            result["steps"][name] = rc
            if rc != 0:
                failing.append(name)
                result.setdefault("failure_tail", {})[name] = out[-600:]
        result["detected"] = bool(failing)
        result["failing_steps"] = failing
        return result
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(tree)], cwd=repo, capture_output=True)
        shutil.rmtree(tree, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--only", default="")
    ap.add_argument("--skip-core", action="store_true")
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    selected = [m for m in MUTANTS if not args.only or m.mid in args.only.split(",")]
    results = []
    for m in selected:
        t0 = time.time()
        r = probe(args.repo.resolve(), args.base, args.work.resolve(), args.python, m, args.skip_core)
        r["seconds"] = round(time.time() - t0, 1)
        results.append(r)
        status = "ERROR" if "error" in r else ("DETECTED" if r["detected"] else "UNDETECTED")
        print(f"{m.mid} {m.kind:8} {status:10} {','.join(r.get('failing_steps', [])) or '-':40} {m.doctrine}", flush=True)
    if args.json:
        args.json.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
