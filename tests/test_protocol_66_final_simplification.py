"""Protocol 6.6 final simplification: structural routing-preservation oracle (workplan 16.11.3).

The frozen map `qualification/ssdp66/eval/routing-preservation-map.yaml` records every direct
route of each consumed entrypoint at the redesigned basis 47dc85d. These checks establish only
that the consumed `dist/skills/*/SKILL.md` keep each target and its discriminating predicate
terms, exclusions and role-local authority boundary. Materially equivalent trigger semantics
remain a Review question; live route probes are Stage F/G evidence.
"""
from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAP = yaml.safe_load((ROOT / "qualification/ssdp66/eval/routing-preservation-map.yaml").read_text(encoding="utf-8"))
LINK_RE = re.compile(r"\[[^\]]*\]\(((?:references|templates)/[A-Za-z0-9_.-]+\.md)\)")
FRONT_RE = re.compile(r"\A---\n.*?\n---\n", re.S)


def consumed(name: str) -> str:
    return (ROOT / "dist" / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


def flat(text: str) -> str:
    return " ".join(LINK_RE.sub(" ", text).lower().replace("**", "").replace("`", "").split())


def clauses(text: str) -> list[tuple[set[str], str]]:
    """(targets linked, link-stripped predicate text) for each line segment split at ';'."""
    out = []
    for line in text.splitlines():
        for segment in line.split(";"):
            targets = set(LINK_RE.findall(segment))
            if targets:
                out.append((targets, flat(segment)))
    return out


def route_holds(text: str, target: str, terms: list[str]) -> bool:
    return any(target in targets and all(term in predicate for term in terms) for targets, predicate in clauses(text))


def git_show(ref: str, rel: str) -> str | None:
    proc = subprocess.run(["git", "-C", str(ROOT), "show", f"{ref}:{rel}"], capture_output=True)
    return proc.stdout.decode("utf-8") if proc.returncode == 0 else None


class RoutingPreservationMap(unittest.TestCase):
    def test_map_covers_every_basis_direct_route(self) -> None:
        for name, spec in MAP["skills"].items():
            basis = git_show(MAP["basis"], f"dist/skills/{name}/SKILL.md")
            if basis is None:
                self.skipTest("basis entrypoints are not resolvable in this clone")
            mapped = {row["target"] for row in spec["routes"]} | {row["target"] for row in MAP["entry_contract"]["routes"]}
            with self.subTest(skill=name):
                self.assertEqual(set(LINK_RE.findall(basis)), mapped)
                for row in spec["routes"]:
                    self.assertIn(row["concern"], MAP["concerns"])
                    self.assertEqual(MAP["concerns"][row["concern"]]["target"], row["target"])
                    self.assertIn(row["disposition"], MAP["dispositions"])

    def test_consumed_entrypoints_keep_exactly_the_basis_direct_routes(self) -> None:
        for name, spec in MAP["skills"].items():
            mapped = {row["target"] for row in spec["routes"]} | {row["target"] for row in MAP["entry_contract"]["routes"]}
            with self.subTest(skill=name):
                self.assertEqual(set(LINK_RE.findall(consumed(name))), mapped)

    def test_every_route_keeps_its_discriminating_predicate(self) -> None:
        for name, spec in MAP["skills"].items():
            text = consumed(name)
            for row in [*spec["routes"], *MAP["entry_contract"]["routes"]]:
                with self.subTest(skill=name, target=row["target"]):
                    self.assertTrue(route_holds(text, row["target"], row["terms"]), row["terms"])

    def test_gates_exclusions_and_authority_boundaries_survive(self) -> None:
        for name, spec in MAP["skills"].items():
            text = flat(consumed(name))
            for group in ("gates", "exclusions", "authority"):
                for term in spec[group]:
                    with self.subTest(skill=name, group=group, term=term):
                        self.assertIn(term, text)
            for term in MAP["entry_contract"]["version_semantics"]:
                with self.subTest(skill=name, version_term=term):
                    self.assertIn(term, text)

    def test_no_forbidden_eager_route(self) -> None:
        for name in MAP["skills"]:
            for target in MAP["forbidden_direct_routes"]:
                with self.subTest(skill=name, target=target):
                    self.assertNotIn(f"]({target})", consumed(name))

    def test_catalog_frontmatter_is_unchanged_from_basis(self) -> None:
        for name in MAP["skills"]:
            basis = git_show(MAP["basis"], f"dist/skills/{name}/SKILL.md")
            if basis is None:
                self.skipTest("basis entrypoints are not resolvable in this clone")
            with self.subTest(skill=name):
                self.assertEqual(FRONT_RE.match(consumed(name)).group(0), FRONT_RE.match(basis).group(0))

    def test_predicate_oracle_rejects_label_only_or_weakened_routes(self) -> None:
        text = consumed("software-implementation")
        row = next(r for r in MAP["skills"]["software-implementation"]["routes"] if r["concern"] == "pem")
        self.assertTrue(route_holds(text, row["target"], row["terms"]))
        # the label alone cannot carry the predicate
        self.assertFalse(route_holds("- [project history recurrence mature](references/project-engineering-memory.md)", row["target"], row["terms"]))
        # dropping one discriminating trigger fails
        weakened = text.replace("memory-bound", "")
        self.assertFalse(route_holds(weakened, row["target"], row["terms"]))
        # moving the predicate away from its link fails
        self.assertFalse(route_holds("project history mature recurrence optimization/scaling migration/recovery/revert memory-bound;"
                                     " see [PEM](references/project-engineering-memory.md)", row["target"], row["terms"]))


if __name__ == "__main__":
    unittest.main()
