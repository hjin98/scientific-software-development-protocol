#!/usr/bin/env python3
"""Run the Core acceptance suite, sharded across processes.

Most test modules are independent and run concurrently in separate interpreters.
Resource-heavy installed-artifact acceptance runs as an exclusive leading shard
because it builds and installs wheel/sdist artifacts in multiple virtual
environments.  CI qualification showed that this shard is stable from a clean
runner but can fail after a parallel predecessor pool, so it is deliberately
executed before the pool rather than coupled to residual runner state/resources.

Concurrency for the remaining shards is sized from the machine's effective CPU
allocation and capped by the parallel module count.

Usage:
    python orchestrator/scripts/run_core_tests.py [-j N] [module ...]
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = PACKAGE_ROOT / "tests"
SOURCE_DIR = PACKAGE_ROOT / "src"
EXCLUSIVE_MODULES = frozenset({"tests.test_installed_product"})


def effective_cpus() -> int:
    """Prefer the scheduler's actual allocation over the machine's core count."""

    try:
        return max(1, len(os.sched_getaffinity(0)))  # type: ignore[attr-defined]
    except (AttributeError, OSError):
        return max(1, os.cpu_count() or 1)


def discover() -> list[str]:
    return sorted(
        f"tests.{path.stem}" for path in TESTS_DIR.glob("test_*.py")
    )


def run_module(module: str) -> tuple[str, int, str, float]:
    started = time.monotonic()
    environment = dict(os.environ)
    pythonpath = [str(SOURCE_DIR)]
    if environment.get("PYTHONPATH"):
        pythonpath.append(environment["PYTHONPATH"])
    environment["PYTHONPATH"] = os.pathsep.join(pythonpath)
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "unittest", "-v", module],
        cwd=str(PACKAGE_ROOT),
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    return module, result.returncode, result.stdout + result.stderr, time.monotonic() - started


def _record_result(
    result: tuple[str, int, str, float],
    failures: list[tuple[str, str]],
) -> int:
    module, code, output, elapsed = result
    count = _test_count(output)
    status = "ok" if code == 0 else f"FAIL({code})"
    print(f"  {status:>8}  {module:<48} {count:>4} tests  {elapsed:5.1f}s")
    if code != 0:
        failures.append((module, output))
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modules", nargs="*", help="test modules (default: all)")
    parser.add_argument(
        "-j", "--jobs", type=int, default=None, help="worker processes (default: effective CPUs)"
    )
    args = parser.parse_args()

    modules = args.modules or discover()
    if not modules:
        print("no test modules found", file=sys.stderr)
        return 1

    exclusive = [module for module in modules if module in EXCLUSIVE_MODULES]
    parallel = [module for module in modules if module not in EXCLUSIVE_MODULES]
    requested_jobs = args.jobs or effective_cpus()
    jobs = min(requested_jobs, len(parallel)) if parallel else 0

    description = f"running {len(modules)} test modules"
    if exclusive:
        description += f" with {len(exclusive)} leading exclusive shard(s)"
    if parallel:
        description += f" and {len(parallel)} parallel shard(s) across {jobs} worker(s)"
    print(description)

    failures: list[tuple[str, str]] = []
    total = 0
    started = time.monotonic()

    # Run installed-artifact acceptance from clean runner state.  It is the
    # installed product's acceptance owner and intentionally does substantial
    # wheel/sdist/venv work; predecessor pools must not affect that observation.
    for module in exclusive:
        total += _record_result(run_module(module), failures)

    if parallel:
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            for result in pool.map(run_module, parallel):
                total += _record_result(result, failures)

    elapsed = time.monotonic() - started
    for module, output in failures:
        print(f"\n{'=' * 70}\n{module}\n{'=' * 70}\n{output}")
    print(
        f"\n{total} tests across {len(modules)} modules in {elapsed:.1f}s "
        f"-- {'FAILED: ' + ', '.join(m for m, _ in failures) if failures else 'OK'}"
    )
    return 1 if failures else 0


def _test_count(output: str) -> int:
    for line in output.splitlines():
        if line.startswith("Ran ") and " test" in line:
            try:
                return int(line.split()[1])
            except (IndexError, ValueError):  # pragma: no cover
                return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
