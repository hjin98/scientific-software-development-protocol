"""Skills-only 7.2 candidate, S1 (workplan SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2, O-1 to O-5).

Structural checks, necessary and not sufficient: they cannot show that agents behave as the doctrine
requires, and the lossless mapping they run is the D4 author's mapping, whose independent check is a
separate context's record.
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
sys.path.insert(0, str(SOURCE))
import build_skills  # noqa: E402
import validate_packages  # noqa: E402

ACCEPTED_66 = "22f4bdba53795da3a6f13f162529f3a843fc37ae"
QUAL = ROOT / "qualification" / "ssdp70" / "qual-v2"
MAPPING = json.loads((QUAL / "frozen-minimum-mapping.json").read_text(encoding="utf-8"))
WORKPLAN = ROOT / "workplans" / "active" / "SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md"
OWNER = SOURCE / "shared" / "references" / "scientific-inspectability-and-initiative.md"
FRAGMENT = build_skills.CHECKS_FRAGMENT.read_text(encoding="utf-8")
BLOCK_SKILLS = tuple(MAPPING["route_groups"]["all"])
ALL_SKILLS = (*BLOCK_SKILLS, "repository-hygiene")
ROLE_NAMES = set(MAPPING["route_groups"]["roles"])


def source_path(name: str) -> Path:
    kind = "roles" if name in ROLE_NAMES else "specialists"
    return SOURCE / kind / name / "SKILL.md"


def generated(name: str) -> str:
    """The entrypoint text the build produces for the Scientific checks (marker expanded)."""
    path = source_path(name)
    return build_skills.expand_checks(path.read_text(encoding="utf-8"), FRAGMENT, str(path))


def accepted(rel: str) -> str | None:
    proc = subprocess.run(["git", "-C", str(ROOT), "show", f"{ACCEPTED_66}:{rel}"], capture_output=True)
    return proc.stdout.decode("utf-8") if proc.returncode == 0 else None


def normalized(text: str) -> str:
    return " ".join(text.split())


def block_of(text: str) -> str:
    """The generated section: from its heading to the next level-2 heading."""
    start = text.index("## Scientific checks\n")
    end = text.index("\n## ", start + 1)
    return text[start:end].rstrip("\n")


def independent_subset(fragment: str, questions: str, elements: str) -> str:
    """A second, deliberately naive filter of the fragment, to compare with the build's renderer."""
    out = []
    for line in fragment.rstrip("\n").split("\n"):
        tag = re.match(r"\{\{([qe])=([^}]*)\}\} ", line)
        if tag:
            chosen = questions if tag.group(1) == "q" else elements
            if not any(v in chosen for v in tag.group(2).split(",")):
                continue
            line = line[tag.end():]
        for inline in re.finditer(r"\{\{(!?)q=([^:}]*):(.*?)\}\}", line):
            keep = any(v in questions for v in inline.group(2).split(",")) != bool(inline.group(1))
            line = line.replace(inline.group(0), inline.group(3) if keep else "")
        out.append(line)
    return "\n".join(out)


def marker(questions: str, elements: str) -> str:
    return f"<!-- SSDP-SCIENTIFIC-CHECKS q={','.join(questions)} e={','.join(elements)} -->"


class InjectionTests(unittest.TestCase):
    def test_marker_selection_per_entrypoint_matches_the_role_map(self) -> None:
        for name in ALL_SKILLS:
            selection = build_skills.checks_selection(source_path(name).read_text(encoding="utf-8"), name)
            expected = MAPPING["role_map"][name]
            if not expected["elements"]:
                self.assertIsNone(selection, name)
                continue
            self.assertEqual(("".join(sorted(selection[0])), "".join(sorted(selection[1]))),
                             ("".join(sorted(expected["questions"])), "".join(sorted(expected["elements"]))), name)

    def test_generated_block_equals_its_fragment_subset(self) -> None:
        for name in BLOCK_SKILLS:
            roles = MAPPING["role_map"][name]
            self.assertEqual(block_of(generated(name)),
                             independent_subset(FRAGMENT, roles["questions"], roles["elements"]), name)
        with tempfile.TemporaryDirectory() as td:
            build_skills.build(Path(td))
            for name in BLOCK_SKILLS:
                built = (Path(td) / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertEqual(block_of(built), block_of(generated(name)), name)
                self.assertNotIn(build_skills.CHECKS_MARKER, built, name)
                self.assertNotIn("{{", built, name)
            self.assertNotIn("Scientific checks", (Path(td) / "skills" / "repository-hygiene" / "SKILL.md").read_text(encoding="utf-8"))

    def test_the_owner_route_survives_injection_into_the_package_payload(self) -> None:
        for name in BLOCK_SKILLS:
            spec = {**build_skills.ROLE_SPECS, **build_skills.SPECIALIST_SPECS}[name]
            self.assertIn("scientific-inspectability-and-initiative.md", spec["references"], name)

    def test_unknown_tags_fail(self) -> None:
        for bad in (marker("FRX", "1"), marker("FR", "9")):
            with self.assertRaises(SystemExit, msg=bad):
                build_skills.expand_checks(f"head\n{bad}\n", FRAGMENT, "x")
        with self.assertRaises(SystemExit):
            build_skills.validate_checks_fragment(FRAGMENT.replace("{{e=2}}", "{{e=8}}", 1))
        with self.assertRaises(SystemExit):
            build_skills.validate_checks_fragment(FRAGMENT.replace("{{q=T}}", "{{q=Z}}", 1))
        with self.assertRaises(SystemExit):
            build_skills.validate_checks_fragment(FRAGMENT.replace("{{q=V: or no selection}}", "{{q=Y: or no selection}}", 1))

    def test_malformed_and_unreferenced_inputs_fail(self) -> None:
        with self.assertRaises(SystemExit):
            build_skills.expand_checks("<!-- SSDP-SCIENTIFIC-CHECKS q=F e= -->", FRAGMENT, "x")
        with self.assertRaises(SystemExit):
            build_skills.expand_checks(f"{marker('F', '3')}\n", FRAGMENT, "x")  # element 3 needs element 1
        with self.assertRaises(SystemExit):
            build_skills.expand_checks(f"{marker('F', '16')}\n", FRAGMENT, "x")  # element 6 needs element 4
        with self.assertRaises(SystemExit):
            build_skills.validate_checks_fragment(FRAGMENT.replace("{{e=7}} ", "", 1))  # element 7 loses its carrier
        with self.assertRaises(SystemExit):
            build_skills.render_checks("{{q=F}} text {{q=V:open", {"F"}, {"1"})

    def test_duplicate_marker_fails(self) -> None:
        text = f"a\n{marker('FR', '14')}\nb\n{marker('FR', '14')}\n"
        with self.assertRaises(SystemExit):
            build_skills.expand_checks(text, FRAGMENT, "x")

    def test_registry_requires_exactly_one_marker_except_hygiene(self) -> None:
        def registry(skill_name: str, body: str) -> None:
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                skill = root / skill_name
                (skill / "agents").mkdir(parents=True)
                (skill / "agents" / "openai.yaml").write_text("x: y\n", encoding="utf-8")
                (skill / "SKILL.md").write_text(
                    f"---\nname: {skill_name}\n---\n\n{build_skills.ENTRY_PLACEHOLDER}\n\n{body}", encoding="utf-8")
                specs = {skill_name: {"role": "x", "references": [], "templates": []}}
                with mock.patch.object(build_skills, "ROLES", root):
                    build_skills.validate_registry(root, specs, "role")

        registry("software-design", marker("FR", "14") + "\n")  # one marker: accepted
        with self.assertRaises(SystemExit):
            registry("software-design", "no marker here\n")  # missing marker
        with self.assertRaises(SystemExit):
            registry("software-design", marker("FR", "14") + "\n" + marker("FR", "14") + "\n")  # duplicate marker
        registry("repository-hygiene", "no marker here\n")  # hygiene carries none
        with self.assertRaises(SystemExit):
            registry("repository-hygiene", marker("FR", "14") + "\n")  # and must not gain one


class IndependentValidationTests(unittest.TestCase):
    """The independent package validator re-derives the generated block itself."""

    def test_validator_accepts_the_built_bundle_and_rejects_block_drift(self) -> None:
        for name in ("software-design", "software-documentation", "repository-hygiene"):
            kind = "role" if name in ROLE_NAMES else "specialist"
            root = ROOT / "dist" / "skills" / name
            files = validate_packages.directory_files(root)
            self.assertEqual(validate_packages.validate_core_bundle(dict(files), name, kind, source_path(name).parent), [], name)
            if name == "repository-hygiene":
                continue
            drifted = dict(files)
            drifted["SKILL.md"] = files["SKILL.md"].replace(b"These checks are the complete obligation", b"These checks are optional", 1)
            self.assertTrue(validate_packages.validate_core_bundle(drifted, name, kind, source_path(name).parent), name)
            unexpanded = dict(files)
            unexpanded["SKILL.md"] = files["SKILL.md"] + b"\n<!-- SSDP-SCIENTIFIC-CHECKS q=F e=1 -->\n"
            self.assertTrue(any("unexpanded" in e for e in validate_packages.validate_core_bundle(unexpanded, name, kind, source_path(name).parent)))


class ByteIdentityTests(unittest.TestCase):
    """O-2: the 6.6 text is byte-identical outside the block, in source and in generated dist."""

    def setUp(self) -> None:
        if accepted("source/shared/references/abstraction-and-concretization.md") is None:
            self.skipTest("accepted 6.6 ref unavailable in this clone")

    @staticmethod
    def _strip_sanctioned(lines: list[str], skill: str) -> list[str]:
        out = []
        for line in lines:
            if line.startswith("**Governing version.**"):
                line = "**Governing version.**"
            if skill == "software-implementation" and line.startswith("description: "):
                line = "description: "
            out.append(line)
        return out

    def test_source_entrypoints_equal_66_apart_from_marker_and_description(self) -> None:
        for name in ALL_SKILLS:
            kind = "roles" if name in ROLE_NAMES else "specialists"
            base = accepted(f"source/{kind}/{name}/SKILL.md").split("\n")
            current = source_path(name).read_text(encoding="utf-8").split("\n")
            if name in BLOCK_SKILLS:
                marks = [i for i, line in enumerate(current) if line.startswith(build_skills.CHECKS_MARKER)]
                self.assertEqual(len(marks), 1, name)
                self.assertEqual(current[marks[0] + 1], "", name)
                del current[marks[0]:marks[0] + 2]
            self.assertEqual(self._strip_sanctioned(current, name), self._strip_sanctioned(base, name), name)

    def test_generated_dist_entrypoints_equal_66_outside_the_block(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            build_skills.build(Path(td))
            for name in ALL_SKILLS:
                base = accepted(f"dist/skills/{name}/SKILL.md").split("\n")
                current = (Path(td) / "skills" / name / "SKILL.md").read_text(encoding="utf-8").split("\n")
                if name in BLOCK_SKILLS:
                    start = current.index("## Scientific checks")
                    end = next(i for i in range(start + 1, len(current)) if current[i].startswith("## "))
                    del current[start:end]
                self.assertEqual(self._strip_sanctioned(current, name), self._strip_sanctioned(base, name), name)

    def test_committed_dist_carries_the_generated_block(self) -> None:
        for name in BLOCK_SKILLS:
            committed = (ROOT / "dist" / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertEqual(block_of(committed), block_of(generated(name)), name)


class BlockSizeReportTests(unittest.TestCase):
    """O-4 (SD-R13): sizes against the 7.1 reference; excess only for required content new to this surface."""

    def test_excess_over_the_71_block_is_attributed_to_the_inaccessible_home_rule(self) -> None:
        spec = importlib.util.spec_from_file_location("measure_blocks", QUAL / "measure_blocks.py")
        measure = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(measure)
        if accepted("dist/skills/software-implementation/SKILL.md") is None:
            self.skipTest("accepted 6.6 ref unavailable in this clone")
        with tempfile.TemporaryDirectory() as td:
            build_skills.build(Path(td))
            report = measure.measure(Path(td) / "skills")
        for name, row in report.items():
            self.assertNotIn("UNATTRIBUTED", row["parts"], name)
            self.assertEqual(sum(row["parts"].values()), row["block_bytes"], name)
            self.assertLessEqual(row["excess_over_100_percent"], row["new_required_content_bytes"],
                                 f"{name}: excess over the 7.1 block must be lossless required content absent from 7.1")
            self.assertEqual(row["new_required_content_bytes"] > 0, MAPPING["role_map"][name]["elements"].find("3") >= 0, name)


class LosslessMappingTests(unittest.TestCase):
    """O-3: every mapped phrase exists in each route it lists; the role map and numbering hold."""

    def texts(self) -> dict[str, str]:
        return {name: normalized(generated(name)) for name in BLOCK_SKILLS}

    def test_every_mapped_phrase_exists_in_every_listed_route(self) -> None:
        texts, groups = self.texts(), MAPPING["route_groups"]
        for item in MAPPING["items"]:
            routes = groups[item["routes"]] if isinstance(item["routes"], str) else item["routes"]
            for name in routes:
                for phrase in item["phrases"]:
                    self.assertIn(normalized(phrase), texts[name], f"{item['id']} missing from {name}")
                for phrase in item.get("absent_phrases", []):
                    self.assertNotIn(normalized(phrase), texts[name], f"{item['id']} unexpectedly in {name}")

    def test_mapped_phrases_do_not_appear_outside_their_routes_when_element_specific(self) -> None:
        texts, groups = self.texts(), MAPPING["route_groups"]
        for item in MAPPING["items"]:
            routes = groups[item["routes"]] if isinstance(item["routes"], str) else item["routes"]
            if not item["id"].startswith(("E3.", "E5.", "E6.", "E7.", "Q.variants", "Q.tensions", "L.variant", "L.inaccessible")):
                continue
            for name in set(BLOCK_SKILLS) - set(routes):
                for phrase in item["phrases"]:
                    self.assertNotIn(normalized(phrase), texts[name], f"{item['id']} leaks into {name}")

    def test_role_map_elements_questions_and_visible_numbering(self) -> None:
        for name in ALL_SKILLS:
            roles = MAPPING["role_map"][name]
            text = generated(name)
            if not roles["elements"]:
                self.assertNotIn("Scientific checks", text, name)
                continue
            block = block_of(text)
            self.assertEqual("".join(re.findall(r"(?m)^([1-7])\. \*\*", block)), roles["elements"], name)
            self.assertEqual(len(re.findall(r'(?m)^- (?:"|Only if it relies)', block)), len(roles["questions"]), name)
            self.assertIn("\n1. **Findings.**", block, name)
            self.assertIn("\n4. **Claims and scope.**", block, name)  # elements 3 and 6 refer back to 1 and 4
            if "3" in roles["elements"]:
                self.assertIn("as in element 1", block, name)
            if "6" in roles["elements"]:
                self.assertIn("exact element-4 source", block, name)

    def test_every_label_table_row_and_the_new_row_is_mapped(self) -> None:
        text = WORKPLAN.read_text(encoding="utf-8")
        table = text.split("**Consumed-surface label meanings (frozen minimum).**", 1)[1].split("- **Specialist placement (frozen).**", 1)[0]
        labels = [m.group(1).strip() for m in re.finditer(r"(?m)^  \| (.+?) \|", table)
                  if m.group(1).strip() not in {"Label", "---"}]
        self.assertGreaterEqual(len(labels), 21)
        self.assertIn("inaccessible home (element 3)", labels)
        mapped = " ".join(item["frozen"] for item in MAPPING["items"])
        for label in labels:
            self.assertIn(f"'{label}'", mapped, f"label-table row {label!r} has no mapping item")


class ConsistencyTests(unittest.TestCase):
    """O-5: no current text makes an owner read mandatory or describes an owner-load trigger on the entrypoint."""

    LEGACY = re.compile(
        r"owner-load trigger|owner load trigger|load trigger|Load the scientific-inspectability owner"
        r"|loads? the scientific-inspectability owner|R2 governs loading|scientific inspectability -> \[owner\]",
        re.I,
    )

    def test_owner_entrypoints_and_readmes_have_no_mandatory_owner_read(self) -> None:
        files = [OWNER, ROOT / "README.md", SOURCE / "README.md", *[source_path(n) for n in ALL_SKILLS]]
        for path in files:
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                self.assertIsNone(self.LEGACY.search(line), f"{path.relative_to(ROOT)}:{number}: {line[:100]}")
        for name in BLOCK_SKILLS:
            self.assertIsNone(self.LEGACY.search(generated(name)), name)

    def test_owner_states_optional_depth_and_the_named_exception(self) -> None:
        owner = OWNER.read_text(encoding="utf-8")
        self.assertIn("This owner is optional depth and no load is required.", owner)
        self.assertIn("Apart from the (a)–(c) blocking conditions", owner)
        self.assertNotIn("It is not inlined.", owner)
        self.assertIn("**Predicate without a depth read.**", owner)

    def test_governing_workplan_amendments_are_in_place(self) -> None:
        text = WORKPLAN.read_text(encoding="utf-8")
        lines = text.splitlines()
        self.assertTrue(any(line.startswith("**Skills-only 7.2 amendment (2026-10-07;") for line in lines))
        anchors = (
            "**Current stakeholder fixed-cost decision (2026-09-28).**",
            "   - The family must reach a final PASS on **every** §3-ordered criterion",
            "   - Any non-PASS final criterion state blocks qualification PASS",
            "### 8.2 Obligation predicate and owner depth-read points",
            "  - one routing line carrying **R1**",
            "  - one clause in its Completion/report contract",
            "  - *Selection or placement miss*",
            "   - Structural checks (single owner",
            "- Create the new owner with the §3.1 terms",
            "Apply §8.3 to the four role entrypoints",
            "- an entrypoint/predicate placement that misses ordinary D4 work",
            "13. The §8.2 obligation predicate",
            "14. §11 qualification passes both absolute adequacy floors",
            "16. Accepted 6.6 capabilities are preserved losslessly",
            "- placement or selection misses ordinary work",
        )
        for anchor in anchors:
            found = [line for line in lines if line.startswith(anchor)]
            self.assertEqual(len(found), 1, anchor)
            self.assertIn("[7.2 amendment", found[0], anchor)
        self.assertIn("| inaccessible home (element 3) |", text)
        self.assertNotIn("the (a)-(c) blocking conditions and coverage-envelope detail", text)
        self.assertNotIn("The owner's doctrine is not inlined (I66-3).", text)
        self.assertIn("## 11. Qualification design (cold contract created in Stage A)\n\n[7.2 amendment", text)

    def test_current_placement_text_in_the_governing_workplan_is_annotated_or_amended(self) -> None:
        text = WORKPLAN.read_text(encoding="utf-8")
        section = text.split("### 8.2 ", 1)[1].split("\n## 9.", 1)[0]
        for number, line in enumerate(section.splitlines(), 1):
            if self.LEGACY.search(line):
                self.assertIn("[7.2 amendment", line, f"section 8.2-8.3 line {number} states the old trigger unannotated")
        self.assertNotIn("R2 governs loading", section)
        self.assertNotIn("loads the owner", section)


if __name__ == "__main__":
    unittest.main()
