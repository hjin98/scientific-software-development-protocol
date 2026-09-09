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


def section(text: str, heading: str, next_level: str = "## ") -> str:
    start = text.index(heading)
    body = text[start + len(heading):]
    pos = body.find("\n" + next_level)
    return body if pos < 0 else body[:pos]


def language_route_links(role_path: str) -> set[str]:
    text = read(role_path)
    block = section(text, "### Language-profile dispatch", "### ")
    return {Path(link).name for link in LINK_RE.findall(block)}


class Protocol515LanguageProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.router = read("source/shared/references/language-profiles.md").lower()
        self.python = read("source/shared/references/python-engineering.md").lower()
        self.cpp = read("source/shared/references/cpp-engineering.md").lower()
        self.performance = read("source/shared/references/performance-and-parallelism.md").lower()
        self.qualification = read("qualification/tool-routing/SCENARIOS.md").lower()
        self.design_path = "source/roles/software-design/SKILL.md"
        self.impl_path = "source/roles/software-implementation/SKILL.md"

    def test_shared_profile_direction_rejects_global_language_precedence(self) -> None:
        self.assertRegex(self.router, r"shared domain rule\s*->\s*active language profile\(s\)\s*->\s*implementation-local realization")
        self.assertIn("shared owners remain canonical", self.router)
        self.assertIn("current protocol 6 domain doctrine is authoritative", self.router)
        self.assertNotIn("shared protocol 5 doctrine remains authoritative", self.router)
        forbidden = (
            r"python(?: profile)?\s+(?:globally\s+)?(?:outranks|overrides|takes precedence over)\s+c\+\+",
            r"c\+\+(?: profile)?\s+(?:globally\s+)?(?:outranks|overrides|takes precedence over)\s+python",
            r"profile(?:s)?\s+(?:may|can|must)\s+(?:override|weaken)\s+shared",
        )
        for pattern in forbidden:
            self.assertIsNone(re.search(pattern, self.router), pattern)

    def test_material_routes_are_mandatory_and_composed(self) -> None:
        design_links = language_route_links(self.design_path)
        impl_links = language_route_links(self.impl_path)
        self.assertEqual(design_links, impl_links)
        self.assertEqual(3, len(design_links))
        for path in (self.design_path, self.impl_path):
            block = section(read(path), "### Language-profile dispatch", "### ")
            for name in design_links:
                line = next(line for line in block.splitlines() if name in line)
                self.assertIn("MUST read", line, (path, name))
        self.assertIn("must read both", self.router)
        self.assertIn("do not infer a global python-over-c++ or c++-over-python precedence", self.router)

    def test_real_package_builder_carries_only_routed_profile_payload(self) -> None:
        routed = language_route_links(self.design_path)
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "dist"
            subprocess.run([sys.executable, str(ROOT / "source/build_skills.py"), "--output", str(out)], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for role in ("software-design", "software-implementation"):
                refs = {p.name for p in (out / "skills" / role / "references").iterdir() if p.is_file()}
                self.assertTrue(routed <= refs, (role, sorted(routed - refs)))
            for specialist in ("software-documentation", "repository-hygiene", "software-maintenance-audit"):
                refs = {p.name for p in (out / "skills" / specialist / "references").iterdir() if p.is_file()}
                self.assertTrue(routed.isdisjoint(refs), (specialist, sorted(routed & refs)))

    def test_python_runtime_selection_is_not_gil_monoculture(self) -> None:
        runtime = section(self.python, "## interpreter/runtime and concurrency")
        for token in ("gil-constrained", "free-threaded", "alternative interpreters", "when a gil is active", "when free-threading is active", "asynchronous/event-loop"):
            self.assertIn(token, runtime)
        self.assertNotIn("python => gil => processes", runtime)

    def test_python_accelerator_counterfactual_is_gated_and_complete(self) -> None:
        accel = section(self.python, "## architecture-gated accelerator realization")
        for concept in ("dormant unless", "cpu-only", "when enabled", "dtype and precision", "cpu/reference", "transfer", "synchronization", "device-memory", "packaging/runtime/device compatibility", "shared performance and scientific owners", "examples rather than required identities", "accepted d3 architecture"):
            self.assertIn(concept, accel)
        self.assertNotRegex(accel, r"(?:always|universally)\s+(?:require|enable|use).{0,30}(?:gpu|accelerator|cuda)")

    def test_cpp_accelerator_uses_same_shared_gate(self) -> None:
        accel = section(self.cpp, "## accelerator realization")
        for concept in ("dormant unless", "accepted d3 architecture", "when enabled", "central-processing-unit (cpu)/reference numerical equivalence", "end-to-end benefit"):
            self.assertIn(concept, accel)

    def test_performance_counterfactual_separates_simple_efficiency_from_complexity(self) -> None:
        for token in ("efficiency by construction versus complexity escalation", "without benchmark ceremony", "do not report an unmeasured change as a measured speedup", "new language/native boundary", "explicit simd", "additional async/thread/process/mpi runtime", "accelerator implementation", "require representative evidence before durable adoption"):
            self.assertIn(token, self.performance)

    def test_counterfactual_qualification_covers_direction_not_tool_identity(self) -> None:
        block = section(self.qualification, "## protocol 5.15 language-profile semantic counterfactuals")
        for heading in ("### shared/profile conflict", "### mixed-language precedence", "### python runtime variants", "### accelerator disabled versus enabled", "### performance versus complexity", "### effective allocation", "### language-boundary architecture"):
            self.assertIn(heading, block)
        for token in ("exact prose, profile filenames, framework names, and build-script variable names are not the oracle", "shared owner wins", "neither language has global precedence"):
            self.assertIn(token, block)

    def test_version_binding_and_repository_local_python_remain_preserved(self) -> None:
        versioning = read("source/shared/references/protocol-versioning-and-compatibility.md").lower()
        root_readme = read("README.md").lower()
        self.assertIn("protocol 5.15 is a backward-compatible", versioning)
        self.assertIn("active older workplans do not automatically adopt protocol 5.16 or any later release", versioning)
        self.assertIn("may continue under their declared version", versioning)
        self.assertIn("repository-local delegated d4 validation machinery", root_readme)
        self.assertIn("protocol_version: 5.14.0", read("workplans/archive/PROTOCOL-5.15-LANGUAGE-PROFILES-CPP-PERFORMANCE.md"))


if __name__ == "__main__":
    unittest.main()
