from __future__ import annotations

import json
import os
import posixpath
import re
import unittest
import urllib.error
import urllib.request


BOOTSTRAP_CANDIDATE = "e09a9d1480211eea2d16d722182bb5c6de1bee12"
PUBLIC_ROOT = "https://raw.githubusercontent.com/hjin98/scientific-software-development-protocol"
LOCAL_MD_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md(?:#[^)]*)?)\)")
PROFILE_ROOT = "orchestrator/src/" + "sdp_" + "orchestrator/core/resources/protocol/ssdp-protocol-6.4"
ENTRYPOINTS = (
    "source/roles/scientific-formulation/SKILL.md",
    "source/roles/numerical-algorithm-design/SKILL.md",
    "source/roles/software-design/SKILL.md",
    "source/roles/software-implementation/SKILL.md",
    "source/specialists/software-documentation/SKILL.md",
    "source/specialists/software-maintenance-audit/SKILL.md",
    "source/specialists/repository-hygiene/SKILL.md",
)


class Protocol64BootstrapReadinessTests(unittest.TestCase):
    """Qualify an existing immutable 6.4 snapshot before its public mapping exists."""

    @classmethod
    def setUpClass(cls) -> None:
        if not (os.environ.get("CI") or os.environ.get("SSDP_VALIDATE_PUBLIC_FALLBACK") == "1"):
            raise unittest.SkipTest("exact-ref Protocol 6.4 bootstrap readiness runs in CI or with SSDP_VALIDATE_PUBLIC_FALLBACK=1")
        cls.cache: dict[str, bytes] = {}

    @classmethod
    def fetch_bytes(cls, path: str) -> bytes:
        if path in cls.cache:
            return cls.cache[path]
        url = f"{PUBLIC_ROOT}/{BOOTSTRAP_CANDIDATE}/{path}"
        try:
            with urllib.request.urlopen(url, timeout=20) as response:
                data = response.read()
        except urllib.error.URLError as exc:
            raise AssertionError(
                f"Protocol 6.4 bootstrap candidate cannot resolve {path} at exact ref {BOOTSTRAP_CANDIDATE}: {exc}"
            ) from exc
        cls.cache[path] = data
        return data

    @classmethod
    def fetch(cls, path: str) -> str:
        try:
            return cls.fetch_bytes(path).decode("utf-8")
        except UnicodeDecodeError as exc:
            raise AssertionError(f"expected UTF-8 text at exact-ref path {path}: {exc}") from exc

    def test_exact_ref_is_64_and_self_reference_safe(self) -> None:
        self.assertEqual(self.fetch("source/PROTOCOL_VERSION").strip(), "6.4.0")
        prompts = self.fetch("source/shared/references/development-workflow-prompts.md")
        versioning = self.fetch("source/shared/references/protocol-versioning-and-compatibility.md")
        readme = self.fetch("README.md")

        self.assertIn("CURRENT_PROTOCOL = 6.4.0", prompts)
        self.assertIn("CURRENT_PUBLIC_REF = UNAVAILABLE_PENDING_6_4_BOOTSTRAP", prompts)
        self.assertNotIn(BOOTSTRAP_CANDIDATE, prompts)
        self.assertNotIn(BOOTSTRAP_CANDIDATE, versioning)
        self.assertNotIn(BOOTSTRAP_CANDIDATE, readme)
        self.assertIn("Protocol 6.4 is **proposed, not accepted-current**", versioning)
        self.assertIn("no 6.4 public-source fallback is authorized", versioning.lower())

    def test_exact_ref_profile_and_distribution_identity(self) -> None:
        profile = json.loads(self.fetch(f"{PROFILE_ROOT}/profile.json"))
        self.assertEqual(profile["profile"]["protocol_version"], "6.4.0")
        self.assertEqual(profile["profile"]["profile_id"], "ssdp-protocol-6.4")
        self.assertEqual(profile["profile"]["profile_schema_version"], 2)

        generated_prompts = self.fetch(f"{PROFILE_ROOT}/prompts.md")
        canonical_prompts = self.fetch("source/shared/references/development-workflow-prompts.md")
        self.assertEqual(generated_prompts, canonical_prompts)

        build_index = json.loads(self.fetch("dist/BUILD_INDEX.json"))
        self.assertEqual(build_index["protocol_version"], "6.4.0")
        self.assertEqual(
            set(build_index["lifecycle_roles"]),
            {"scientific-formulation", "numerical-algorithm-design", "software-design", "software-implementation"},
        )
        self.assertEqual(
            set(build_index["specialists"]),
            {"software-documentation", "repository-hygiene", "software-maintenance-audit"},
        )

    def test_exact_ref_current_routes_are_publicly_resolvable(self) -> None:
        queue: list[str] = []
        for entrypoint in ENTRYPOINTS:
            text = self.fetch(entrypoint)
            self.assertIn("references/abstraction-and-concretization.md", text, entrypoint)
            for raw in LOCAL_MD_RE.findall(text):
                target = raw.split("#", 1)[0]
                if target.startswith("references/"):
                    queue.append("source/shared/references/" + target.removeprefix("references/"))
                elif target.startswith("templates/"):
                    queue.append("source/shared/templates/" + target.removeprefix("templates/"))
                else:
                    self.fail(f"unsupported local route at Protocol 6.4 bootstrap candidate: {entrypoint}: {target}")

        seen: set[str] = set()
        while queue:
            path = queue.pop(0)
            if path in seen:
                continue
            seen.add(path)
            text = self.fetch(path)
            base = posixpath.dirname(path)
            for raw in LOCAL_MD_RE.findall(text):
                target = raw.split("#", 1)[0]
                if "://" in target or target.startswith("#"):
                    continue
                resolved = posixpath.normpath(posixpath.join(base, target))
                if not resolved.startswith("source/shared/"):
                    self.fail(f"Protocol 6.4 exact-ref route escapes shared roots: {path} -> {target}")
                queue.append(resolved)

        for required in (
            "source/shared/references/abstraction-and-concretization.md",
            "source/shared/references/scientific-technical-writing.md",
            "source/shared/references/evidence-evolution-and-dependencies.md",
            "source/shared/references/protocol-versioning-and-compatibility.md",
        ):
            self.assertIn(required, seen)

    def test_exact_ref_package_text_surface_matches_64(self) -> None:
        for skill in (
            "scientific-formulation",
            "numerical-algorithm-design",
            "software-design",
            "software-implementation",
            "software-documentation",
            "repository-hygiene",
            "software-maintenance-audit",
        ):
            with self.subTest(skill=skill):
                self.assertEqual(self.fetch(f"dist/skills/{skill}/PROTOCOL_VERSION").strip(), "6.4.0")
                manifest = json.loads(self.fetch(f"dist/skills/{skill}/protocol-manifest.json"))
                self.assertEqual(manifest["protocol_version"], "6.4.0")


if __name__ == "__main__":
    unittest.main()
