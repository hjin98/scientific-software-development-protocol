from __future__ import annotations

import os
import posixpath
import re
import unittest
import urllib.error
import urllib.request
from pathlib import Path


BOOTSTRAP = "1484c1d3caa49d87cc15bc52a5e775399c1dae1b"
PUBLIC_ROOT = "https://raw.githubusercontent.com/hjin98/scientific-software-development-protocol"
LOCAL_MD_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md(?:#[^)]*)?)\)")


class Protocol63BootstrapTests(unittest.TestCase):
    def test_current_public_mapping_is_exact_and_recovery_remains_unavailable(self) -> None:
        root = Path(__file__).resolve().parents[1]
        versioning = (root / 'source/shared/references/protocol-versioning-and-compatibility.md').read_text(encoding='utf-8')
        prompts = (root / 'source/shared/references/development-workflow-prompts.md').read_text(encoding='utf-8')
        portability = (root / 'PORTABILITY.md').read_text(encoding='utf-8')
        readme = (root / 'README.md').read_text(encoding='utf-8')
        self.assertIn(f'6.3.0 public-source bootstrap -> {BOOTSTRAP}', versioning)
        self.assertIn(f'CURRENT_PUBLIC_REF = {BOOTSTRAP}', prompts)
        self.assertIn(f'6.3.0 public bootstrap -> {BOOTSTRAP}', portability)
        self.assertIn(BOOTSTRAP, readme)
        self.assertIn('6.3.0 recovery -> UNAVAILABLE_PENDING_6.3_ACCEPTANCE', portability)
        self.assertNotIn('6.3.0  -> ' + BOOTSTRAP, versioning)

    def test_published_bootstrap_snapshot_is_real_self_reference_safe_and_route_complete(self) -> None:
        if not (os.environ.get("CI") or os.environ.get("SSDP_VALIDATE_PUBLIC_FALLBACK") == "1"):
            self.skipTest("remote Protocol 6.3 bootstrap realization runs in CI or with SSDP_VALIDATE_PUBLIC_FALLBACK=1")

        cache: dict[str, str] = {}

        def fetch(path: str) -> str:
            if path in cache:
                return cache[path]
            url = f"{PUBLIC_ROOT}/{BOOTSTRAP}/{path}"
            try:
                with urllib.request.urlopen(url, timeout=15) as response:
                    text = response.read().decode("utf-8")
            except (urllib.error.URLError, UnicodeDecodeError) as exc:
                self.fail(f"Protocol 6.3 bootstrap cannot resolve {path} at exact ref {BOOTSTRAP}: {exc}")
            cache[path] = text
            return text

        self.assertEqual(fetch("source/PROTOCOL_VERSION").strip(), "6.3.0")

        versioning = fetch("source/shared/references/protocol-versioning-and-compatibility.md")
        prompts = fetch("source/shared/references/development-workflow-prompts.md")
        self.assertNotIn(BOOTSTRAP, versioning)
        self.assertNotIn(BOOTSTRAP, prompts)
        self.assertIn("UNAVAILABLE_PENDING_6.3_BOOTSTRAP_QUALIFICATION", prompts)

        self.assertIn("memory_schema_version: 1", fetch("source/shared/references/project-engineering-memory.md"))
        self.assertIn("memory_schema_version: 1", fetch("source/shared/templates/project_engineering_memory_template.md"))
        self.assertIn("SCHEMA_VERSION = 1", fetch("source/project_engineering_memory.py"))

        entrypoints = (
            "source/roles/scientific-formulation/SKILL.md",
            "source/roles/numerical-algorithm-design/SKILL.md",
            "source/roles/software-design/SKILL.md",
            "source/roles/software-implementation/SKILL.md",
            "source/specialists/software-documentation/SKILL.md",
            "source/specialists/software-maintenance-audit/SKILL.md",
            "source/specialists/repository-hygiene/SKILL.md",
        )
        queue: list[str] = []
        for entrypoint in entrypoints:
            text = fetch(entrypoint)
            self.assertIn("references/abstraction-and-concretization.md", text, entrypoint)
            direct = {target.split("#", 1)[0] for target in LOCAL_MD_RE.findall(text)}
            if entrypoint.endswith(("software-design/SKILL.md", "software-implementation/SKILL.md")):
                self.assertIn("references/project-engineering-memory.md", direct, entrypoint)
            for target in direct:
                if target.startswith("references/"):
                    queue.append("source/shared/references/" + target.removeprefix("references/"))
                elif target.startswith("templates/"):
                    queue.append("source/shared/templates/" + target.removeprefix("templates/"))
                else:
                    self.fail(f"unsupported local entrypoint route at Protocol 6.3 bootstrap: {entrypoint}: {target}")

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
                    self.fail(f"Protocol 6.3 bootstrap local Markdown route escapes shared roots: {path} -> {target}")
                queue.append(resolved)

        self.assertIn("source/shared/references/project-engineering-memory.md", seen)
        self.assertIn("source/shared/templates/project_engineering_memory_template.md", seen)


if __name__ == "__main__":
    unittest.main()
