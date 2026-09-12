from __future__ import annotations

import os
import posixpath
import re
import unittest
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
REFERENCES = SOURCE / "shared" / "references"
TEMPLATES = SOURCE / "shared" / "templates"
ROLES = SOURCE / "roles"
SPECIALISTS = SOURCE / "specialists"
BOOTSTRAP_RE = re.compile(r"6\.2\.0 public-source bootstrap -> ([0-9a-f]{40})")
LOCAL_MD_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md(?:#[^)]*)?)\)")
INVALIDATED_BOOTSTRAP = "1181c2031710c5d343194d87d08543290fded0ab"
PUBLIC_ROOT = "https://raw.githubusercontent.com/hjin98/scientific-software-development-protocol"


def current_public_bootstrap() -> str | None:
    text = (REFERENCES / "protocol-versioning-and-compatibility.md").read_text(encoding="utf-8")
    match = BOOTSTRAP_RE.search(text)
    return match.group(1) if match else None


class Protocol62RepresentationTests(unittest.TestCase):
    def test_current_version_and_nomenclature(self):
        version = tuple(int(part) for part in (SOURCE / "PROTOCOL_VERSION").read_text().strip().split("."))
        self.assertEqual(version[0], 6)
        self.assertGreaterEqual(version, (6, 2, 0))
        self.assertTrue((REFERENCES / "abstraction-and-concretization.md").is_file())
        self.assertFalse((REFERENCES / "abstraction-and-realization.md").exists())
        self.assertTrue((TEMPLATES / "abstraction_concretization_change_plan_template.md").is_file())
        self.assertFalse((TEMPLATES / "abstraction_realization_change_plan_template.md").exists())

    def test_universal_kernel_contains_lossless_representation_contract(self):
        text = (REFERENCES / "abstraction-and-concretization.md").read_text()
        for phrase in (
            "Lossless Representation Rule",
            "governed scope",
            "One detailed owner per generic rule",
            "Use progressive disclosure",
            "Keep cold paths discoverable",
            "Weight attention without weakening acceptance",
            "Do not deduplicate by adjudicating semantics",
        ):
            self.assertIn(phrase, text)

    def test_every_entrypoint_routes_to_current_kernel(self):
        skill_paths = sorted(ROLES.glob("*/SKILL.md")) + sorted(SPECIALISTS.glob("*/SKILL.md"))
        self.assertEqual(len(skill_paths), 7)
        for path in skill_paths:
            with self.subTest(path=path):
                text = path.read_text()
                self.assertIn("references/abstraction-and-concretization.md", text)
                self.assertNotIn("references/abstraction-and-realization.md", text)

    def test_root_roles_delegate_language_and_tool_leaf_routing(self):
        leaf_routes = (
            "references/python-engineering.md",
            "references/cpp-engineering.md",
            "references/tool-serena.md",
            "references/tool-semgrep.md",
            "references/tool-hypothesis.md",
            "references/tool-codeql.md",
        )
        for role in ("software-design", "software-implementation"):
            text = (ROLES / role / "SKILL.md").read_text()
            self.assertIn("references/language-profiles.md", text)
            self.assertIn("references/tool-assisted-engineering.md", text)
            for leaf in leaf_routes:
                with self.subTest(role=role, leaf=leaf):
                    self.assertNotIn(leaf, text)

        language_router = (REFERENCES / "language-profiles.md").read_text()
        self.assertIn("python-engineering.md", language_router)
        self.assertIn("cpp-engineering.md", language_router)
        tool_router = (REFERENCES / "tool-assisted-engineering.md").read_text()
        for leaf in ("tool-serena.md", "tool-semgrep.md", "tool-hypothesis.md", "tool-codeql.md"):
            self.assertIn(leaf, tool_router)

    def test_documentation_specialist_cold_domain_routes_are_resolvable_and_packaged(self):
        text = (SPECIALISTS / "software-documentation" / "SKILL.md").read_text()
        packaged = ROOT / "dist" / "skills" / "software-documentation" / "references"
        for leaf in (
            "security-and-trust-boundaries.md",
            "performance-and-parallelism.md",
            "storage-and-io.md",
            "release-and-distribution.md",
        ):
            with self.subTest(leaf=leaf):
                self.assertIn(f"references/{leaf}", text)
                self.assertTrue((packaged / leaf).is_file())

    def test_navigation_does_not_define_activation_by_package_presence(self):
        for path in (
            ROOT / "README.md",
            ROOT / "PORTABILITY.md",
            SOURCE / "README.md",
            SOURCE / "SEMANTIC_DEPENDENCIES.md",
        ):
            text = path.read_text().lower()
            self.assertIn("package membership", text)
            self.assertIn("activation", text)

    def test_protocol_62_public_fallback_state_is_coherent(self):
        bootstrap = current_public_bootstrap()
        versioning = (REFERENCES / "protocol-versioning-and-compatibility.md").read_text().lower()
        prompt = (REFERENCES / "development-workflow-prompts.md").read_text().lower()
        portability = (ROOT / "PORTABILITY.md").read_text().lower()
        readme = (ROOT / "README.md").read_text().lower()
        surfaces = (versioning, prompt, portability, readme)

        self.assertIn(f"invalidated bootstrap attempt -> {INVALIDATED_BOOTSTRAP}", versioning)
        self.assertNotIn(f"6.2.0 public-source bootstrap -> {INVALIDATED_BOOTSTRAP}", versioning)

        if bootstrap is None:
            for text in surfaces:
                self.assertIn("automatic current-6.2 public fallback is unavailable", text)
            self.assertIn("bootstrap self-reference rule", prompt)
            self.assertNotIn("current 6.2 may fall back", prompt)
        else:
            self.assertNotEqual(bootstrap, INVALIDATED_BOOTSTRAP)
            for text in surfaces:
                self.assertIn(bootstrap, text)
            current_version = (SOURCE / "PROTOCOL_VERSION").read_text().strip()
            if current_version == "6.2.0":
                self.assertIn(f"public_ref = {bootstrap}", prompt)
                self.assertNotIn("automatic current-6.2 public fallback is unavailable", prompt)
            else:
                self.assertIn(f"accepted_6_2_public_ref = {bootstrap}", prompt)
                current = re.search(r"current_public_ref = ([^\s]+)", prompt)
                self.assertIsNotNone(current)
                current_ref = current.group(1)
                self.assertNotEqual(current_ref, "1484c1d3caa49d87cc15bc52a5e775399c1dae1b")
                self.assertTrue(current_ref == "unavailable_pending_replacement_bootstrap" or re.fullmatch(r"[0-9a-f]{40}", current_ref))
            self.assertNotIn("automatic current-6.2 public fallback is unavailable", portability)
            self.assertIn("repository-default bytes are never a substitute", prompt)

    def test_published_protocol_62_bootstrap_remote_snapshot_is_real_and_route_complete(self):
        bootstrap = current_public_bootstrap()
        if bootstrap is None:
            self.skipTest("replacement Protocol 6.2 public bootstrap has not been published yet")
        if not (os.environ.get("CI") or os.environ.get("SSDP_VALIDATE_PUBLIC_FALLBACK") == "1"):
            self.skipTest("remote public-fallback realization runs in CI or with SSDP_VALIDATE_PUBLIC_FALLBACK=1")

        cache: dict[str, str] = {}

        def fetch(path: str) -> str:
            if path in cache:
                return cache[path]
            url = f"{PUBLIC_ROOT}/{bootstrap}/{path}"
            try:
                with urllib.request.urlopen(url, timeout=15) as response:
                    text = response.read().decode("utf-8")
            except (urllib.error.URLError, UnicodeDecodeError) as exc:
                self.fail(f"published bootstrap cannot resolve {path} at exact ref {bootstrap}: {exc}")
            cache[path] = text
            return text

        self.assertEqual(fetch("source/PROTOCOL_VERSION").strip(), "6.2.0")

        entrypoints = (
            "source/roles/scientific-formulation/SKILL.md",
            "source/roles/numerical-algorithm-design/SKILL.md",
            "source/roles/software-design/SKILL.md",
            "source/roles/software-implementation/SKILL.md",
            "source/specialists/software-documentation/SKILL.md",
            "source/specialists/software-maintenance-audit/SKILL.md",
            "source/specialists/repository-hygiene/SKILL.md",
        )
        required_doc_routes = {
            "references/security-and-trust-boundaries.md",
            "references/performance-and-parallelism.md",
            "references/storage-and-io.md",
            "references/release-and-distribution.md",
        }
        queue: list[str] = []
        for entrypoint in entrypoints:
            text = fetch(entrypoint)
            self.assertIn("references/abstraction-and-concretization.md", text, entrypoint)
            direct = {target.split("#", 1)[0] for target in LOCAL_MD_RE.findall(text)}
            if entrypoint.endswith("software-documentation/SKILL.md"):
                self.assertTrue(required_doc_routes.issubset(direct), direct)
            for target in direct:
                if target.startswith("references/"):
                    queue.append("source/shared/references/" + target.removeprefix("references/"))
                elif target.startswith("templates/"):
                    queue.append("source/shared/templates/" + target.removeprefix("templates/"))
                else:
                    self.fail(f"unsupported local entrypoint route at bootstrap: {entrypoint}: {target}")

        seen: set[str] = set()
        while queue:
            path = queue.pop(0)
            if path in seen:
                continue
            seen.add(path)
            text = fetch(path)
            base = posixpath.dirname(path)
            for raw in LOCAL_MD_RE.findall(text):
                target = raw.split("#", 1)[0]
                if "://" in target or target.startswith("#"):
                    continue
                resolved = posixpath.normpath(posixpath.join(base, target))
                if not resolved.startswith("source/shared/"):
                    self.fail(f"bootstrap local Markdown route escapes shared roots: {path} -> {target}")
                queue.append(resolved)

        bootstrap_prompt = fetch("source/shared/references/development-workflow-prompts.md").lower()
        self.assertIn("bootstrap self-reference rule", bootstrap_prompt)
        self.assertIn("repository-default bytes are never a substitute", bootstrap_prompt)

    def test_preservation_evidence_closes_artifacts_and_transformations(self):
        census = ROOT / "qualification" / "ssdp6" / "SSDP-6.2-PRESERVATION-CENSUS.md"
        text = census.read_text()
        self.assertIn("authority: non-normative-evidence", text)
        self.assertIn("## Artifact-level finite census", text)
        self.assertIn("## Transformation-level closure map", text)
        self.assertIn("all 95", text.lower())
        self.assertIn("Protocol 5.0", text)
        self.assertIn("6.1", text)
        self.assertNotIn("| BLOCKING |", text)
        baseline_references = {path.name for path in REFERENCES.glob("*.md")} - {"project-engineering-memory.md"}
        baseline_templates = {path.name for path in TEMPLATES.glob("*.md")} - {"project_engineering_memory_template.md"}
        for name in sorted(baseline_references):
            self.assertIn(f"`{name}`", text, name)
        for name in sorted(baseline_templates):
            self.assertIn(f"`{name}`", text, name)

    def test_current_navigation_uses_new_kernel_path(self):
        current_files = [
            ROOT / "README.md",
            ROOT / "AGENTS.md",
            ROOT / "PORTABILITY.md",
            SOURCE / "README.md",
            SOURCE / "SEMANTIC_DEPENDENCIES.md",
        ]
        for path in current_files:
            text = path.read_text()
            with self.subTest(path=path):
                self.assertIn("abstraction-and-concretization.md", text)
                self.assertNotIn("source/shared/references/abstraction-and-realization.md", text)


    def test_accepted_62_recovery_and_bootstrap_remain_distinct(self):
        recovery = "b59adc77efe6951912cfd705cc43830c58ca27d0"
        bootstrap = "5a062ebc472755607b9dc66d33a5ebbc4b7429aa"
        invalidated = "1181c2031710c5d343194d87d08543290fded0ab"
        versioning = (REFERENCES / "protocol-versioning-and-compatibility.md").read_text()
        portability = (ROOT / "PORTABILITY.md").read_text()
        self.assertIn(f"6.2.0  -> {recovery}", versioning)
        self.assertIn(f"6.2.0 recovery -> {recovery}", portability)
        self.assertIn(f"6.2.0 public-source bootstrap -> {bootstrap}", versioning)
        self.assertIn(f"6.2.0 public bootstrap -> {bootstrap}", portability)
        self.assertNotEqual(recovery, bootstrap)
        self.assertNotEqual(recovery, invalidated)
        self.assertNotIn(f"6.2.0  -> {invalidated}", versioning)


if __name__ == "__main__":
    unittest.main()
