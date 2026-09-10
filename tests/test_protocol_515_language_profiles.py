from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]+\]\((references/[A-Za-z0-9_.-]+\.md)\)")


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class Protocol515LanguageProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.router = read("source/shared/references/language-profiles.md").lower()
        self.python = read("source/shared/references/python-engineering.md").lower()
        self.cpp = read("source/shared/references/cpp-engineering.md").lower()
        self.performance = read("source/shared/references/performance-and-parallelism.md").lower()
        self.qualification = read("qualification/tool-routing/SCENARIOS.md").lower()
        self.design = read("source/roles/software-design/SKILL.md")
        self.impl = read("source/roles/software-implementation/SKILL.md")

    def test_shared_profile_direction_rejects_global_language_precedence(self) -> None:
        self.assertIn("shared domain rule -> language router -> active language profile(s) -> implementation-local concretization", self.router)
        self.assertIn("shared owners remain canonical", self.router)
        self.assertIn("current protocol 6.2", self.router)
        self.assertNotRegex(self.router, r"python(?: profile)?\s+(?:globally\s+)?(?:outranks|overrides)\s+c\+\+")
        self.assertNotRegex(self.router, r"c\+\+(?: profile)?\s+(?:globally\s+)?(?:outranks|overrides)\s+python")

    def test_root_roles_route_to_language_concern_not_leaves(self) -> None:
        for name, text in (("design", self.design), ("implementation", self.impl)):
            direct = {Path(link).name for link in LINK_RE.findall(text)}
            self.assertIn("language-profiles.md", direct, name)
            self.assertNotIn("python-engineering.md", direct, name)
            self.assertNotIn("cpp-engineering.md", direct, name)
        self.assertIn("python-engineering.md", self.router)
        self.assertIn("cpp-engineering.md", self.router)
        self.assertIn("python-only", self.router)
        self.assertIn("c++-only", self.router)
        self.assertIn("read both", self.router)

    def test_real_package_builder_carries_conditional_profiles_without_promoting_activation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "dist"
            subprocess.run(
                [sys.executable, str(ROOT / "source/build_skills.py"), "--output", str(out)],
                cwd=ROOT,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            for role in ("software-design", "software-implementation"):
                refs = {p.name for p in (out / "skills" / role / "references").iterdir() if p.is_file()}
                self.assertIn("language-profiles.md", refs, role)
                self.assertIn("python-engineering.md", refs, role)
                self.assertIn("cpp-engineering.md", refs, role)

        for specialist in ("software-documentation", "repository-hygiene", "software-maintenance-audit"):
            direct = {Path(link).name for link in LINK_RE.findall(read(f"source/specialists/{specialist}/SKILL.md"))}
            self.assertNotIn("python-engineering.md", direct, specialist)
            self.assertNotIn("cpp-engineering.md", direct, specialist)

    def test_python_runtime_selection_is_not_gil_monoculture(self) -> None:
        for token in ("global-interpreter-lock (gil)-constrained", "free-threaded", "alternative interpreters", "when a gil is active", "when free-threading is active", "asynchronous/event-loop"):
            self.assertIn(token, self.python)
        self.assertNotIn("python => gil => processes", self.python)

    def test_python_accelerator_counterfactual_is_gated_and_complete(self) -> None:
        for concept in ("dormant unless", "cpu-only", "when enabled", "dtype and precision", "cpu/reference", "transfer", "synchronization", "device-memory", "packaging/runtime/device compatibility", "accepted d3 architecture"):
            self.assertIn(concept, self.python)
        self.assertNotRegex(self.python, r"(?:always|universally)\s+(?:require|enable|use).{0,30}(?:gpu|accelerator|cuda)")

    def test_cpp_accelerator_uses_same_shared_gate(self) -> None:
        for concept in ("dormant unless", "accepted d3", "when enabled", "cpu/reference numerical equivalence", "end-to-end benefit"):
            self.assertIn(concept, self.cpp)

    def test_cpp_optimization_and_parallelism_capabilities_survive(self) -> None:
        for token in ("blas", "lapack", "fftw", "auto-vectorization", "simd", "avx-512", "openmp", "message passing interface", "mpi", "cuda", "hip", "sycl", "opencl"):
            self.assertIn(token, self.cpp)
        for token in ("representative", "end-to-end", "resource", "parallel"):
            self.assertIn(token, self.performance)

    def test_counterfactual_qualification_still_covers_language_semantics(self) -> None:
        for heading in ("shared/profile conflict", "mixed-language precedence", "python runtime variants", "accelerator disabled versus enabled", "performance versus complexity", "effective allocation", "language-boundary architecture"):
            self.assertIn(heading, self.qualification)
        for token in ("shared owner wins", "neither language has global precedence"):
            self.assertIn(token, self.qualification)

    def test_historical_515_capability_and_workplan_remain_recoverable(self) -> None:
        versioning = read("source/shared/references/protocol-versioning-and-compatibility.md").lower()
        self.assertIn("5.15", versioning)
        self.assertIn("language profiles", versioning)
        self.assertIn("declared version", versioning)
        self.assertIn("protocol_version: 5.14.0", read("workplans/archive/PROTOCOL-5.15-LANGUAGE-PROFILES-CPP-PERFORMANCE.md"))


if __name__ == "__main__":
    unittest.main()
