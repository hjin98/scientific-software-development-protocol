"""Protocol 7.0 structural qualification (workplan section 11.5 structural checks).

These checks are necessary, not sufficient: they cannot show that agents behave as the
doctrine requires. Live behavior is qualified separately under the frozen Protocol 7
qualification contract.
"""

from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
sys.path.insert(0, str(SOURCE))
import build_skills  # noqa: E402

REFS = SOURCE / "shared" / "references"
TEMPLATES = SOURCE / "shared" / "templates"
OWNER = "scientific-inspectability-and-initiative.md"
ACCEPTED_66 = "22f4bdba53795da3a6f13f162529f3a843fc37ae"

ROLES = ("scientific-formulation", "numerical-algorithm-design", "software-design", "software-implementation")
SPECIALISTS = ("software-documentation", "software-maintenance-audit", "repository-hygiene")
ELEMENT_PREFIX = {
    "1": "1. **Findings.**",
    "2": "2. **Variants.**",
    "3": "3. **Tensions.**",
    "4": "4. **Claims and scope.**",
    "5": "5. **Revisions.**",
    "6": "6. **Choices.**",
    "7": "7. **Authority content.**",
}
PLACEMENT = {
    "scientific-formulation": {"1", "2", "3", "4", "5", "6", "7"},
    "numerical-algorithm-design": {"1", "2", "3", "4", "5", "6", "7"},
    "software-design": {"1", "2", "3", "4", "6", "7"},
    "software-implementation": {"1", "2", "3", "4", "6"},
    "software-documentation": {"1", "4", "6"},
    "software-maintenance-audit": {"1", "4"},
    "repository-hygiene": set(),
}
ROUTE_MARK = "scientific inspectability -> [owner](references/scientific-inspectability-and-initiative.md)"
PREDICATE = (
    "> **Obligation predicate.** Protocol 7 obligations apply when the task produces, changes, runs, or reviews software, "
    "pipelines, analyses, models, or reports whose outputs mediate scientific interpretation or scientific decisions"
)
DEPTH_POINTS = "> **Recommended depth-read points.** This owner is optional depth and no load is required."
BLOCK_HEAD = "## Scientific checks"
DELEGATE_HEAD = "**If you delegate**"
LAUNCHED = "any tools or agents you launched"
QUESTIONS = ("Findings", "Realized results", "Variants", "Tensions")
QUESTION_START = {
    "Findings": '- "Report your material findings',
    "Realized results": '- "Did your work, including any tools or agents you launched, produce',
    "Variants": '- "Did your work, including any tools or agents you launched, evaluate',
    "Tensions": "- Only if it relies on accepted D1/D2 authority for a consequential judgment:",
}
QUESTION_QUALIFIERS = {
    "Findings": ("or state that you have none",),
    "Realized results": ("give your null envelope",),
    "Variants": ("including changes made after seeing results, even bug fixes", "held-out reuse"),
    "Tensions": ("a recorded finding bearing on it that has not been raised as a Serious Challenge",
                 "with each record's entries, binding and asserter"),
}
SPECIALIST_QUESTIONS = {"software-documentation": QUESTIONS[:2], "software-maintenance-audit": QUESTIONS[:2]}


def entrypoint(name: str) -> Path:
    kind = "roles" if name in ROLES else "specialists"
    return SOURCE / kind / name / "SKILL.md"


def generated(name: str) -> str:
    """The entrypoint as the build emits it: the Scientific checks marker expanded from the fragment."""
    path = entrypoint(name)
    return build_skills.expand_checks(
        path.read_text(encoding="utf-8"), build_skills.CHECKS_FRAGMENT.read_text(encoding="utf-8"), str(path))


def element_lines(text: str) -> dict[str, str]:
    found = {}
    for key, prefix in ELEMENT_PREFIX.items():
        lines = [line for line in text.splitlines() if line.startswith(prefix)]
        if lines:
            found[key] = lines[0]
    return found


def question_lines(text: str) -> dict[str, str]:
    return {key: line for key, start in QUESTION_START.items() for line in text.splitlines() if line.startswith(start)}


def block_problems(name: str, text: str) -> list[str]:
    """Everything the consumed surface owes this entrypoint that `text` fails to carry (empty when sound)."""
    problems: list[str] = []
    if not PLACEMENT[name]:
        return [f"{name}: carries a Scientific checks section"] if BLOCK_HEAD in text else []
    if text.count(BLOCK_HEAD + "\n") != 1:
        return [f"{name}: Scientific checks section is not present exactly once"]
    block = text[text.index(BLOCK_HEAD):]
    block = block[:block.index("\n## ", 1)]
    if "These checks are the complete obligation" not in block:
        problems.append(f"{name}: scope lost the complete-obligation sentence")
    if DELEGATE_HEAD not in block:
        problems.append(f"{name}: delegate lead lost")
    expected = SPECIALIST_QUESTIONS.get(name, QUESTIONS)
    found = question_lines(block)
    for key in QUESTIONS:
        if key in expected and key not in found:
            problems.append(f"{name}: delegate question {key} missing")
        if key not in expected and key in found:
            problems.append(f"{name}: delegate question {key} must not be carried")
    for key, line in found.items():
        if LAUNCHED not in line:
            problems.append(f"{name}: {key} question lost its launched-work qualifier")
        for qualifier in QUESTION_QUALIFIERS[key]:
            if qualifier not in line:
                problems.append(f"{name}: {key} question lost its qualifier {qualifier!r}")
    for phrase in ("including when nothing returns", "findings always;", "evidently produced, ran and reviewed no realized results"):
        if phrase not in block:
            problems.append(f"{name}: gap rule lost {phrase!r}")
    variants = "variants, for a returned result, with unknown selection history and claim limit" in block
    if variants != ("Variants" in expected):
        problems.append(f"{name}: gap rule variants clause {'missing' if 'Variants' in expected else 'present without a variant question'}")
    elements = element_lines(block)
    for key in sorted(PLACEMENT[name] - set(elements)):
        problems.append(f"{name}: element {key} missing")
    for key in sorted(set(elements) - PLACEMENT[name]):
        problems.append(f"{name}: element {key} must not be carried")
    return problems


def accepted(rel: str) -> str | None:
    proc = subprocess.run(["git", "-C", str(ROOT), "show", f"{ACCEPTED_66}:{rel}"], capture_output=True)
    return proc.stdout.decode("utf-8") if proc.returncode == 0 else None


class Protocol70StructuralTests(unittest.TestCase):
    def test_single_canonical_owner_carries_frozen_predicate_and_depth_points(self) -> None:
        owners = [path.name for path in REFS.glob("*.md") if "Obligation predicate." in path.read_text(encoding="utf-8")]
        self.assertEqual(owners, [OWNER])
        owner = (REFS / OWNER).read_text(encoding="utf-8")
        self.assertIn(PREDICATE, owner)
        self.assertIn(DEPTH_POINTS, owner)
        for bound in (
            "not guaranteed to perform a tension search",
            "reported as given",
            "may escape rename-following history",
            "without verifying claimed authority",
            "non-writing fallback",
        ):
            self.assertIn(bound, owner)

    def test_scientific_checks_and_elements_are_placed_exactly(self) -> None:
        for name, expected in PLACEMENT.items():
            source = entrypoint(name).read_text(encoding="utf-8")
            text = generated(name)
            self.assertEqual(block_problems(name, text), [], name)
            self.assertEqual(set(element_lines(text)), expected, name)
            self.assertNotIn(ROUTE_MARK, text, f"{name}: the 7.1 owner routing bullet is removed")
            self.assertEqual(source.count(build_skills.CHECKS_MARKER), 1 if expected else 0, name)
            if expected:
                self.assertEqual(text.count(BLOCK_HEAD + "\n"), 1, name)
                self.assertNotIn("## Scientific completion", text, name)
                # at the 7.1 completion-clause position: after the contract text, before the closing section
                self.assertLess(text.index("A required check that did not execute" if name == "software-implementation" else "## "), text.index(BLOCK_HEAD), name)
                tail = text[text.index(BLOCK_HEAD):]
                self.assertRegex(tail[1:].split("\n## ", 1)[1].split("\n", 1)[0], r"^(Challenge and completion|Completion|Output)\b", name)

    def test_each_element_has_one_wording_across_entrypoints(self) -> None:
        wordings: dict[str, set[str]] = {}
        for name in PLACEMENT:
            for key, line in element_lines(generated(name)).items():
                wordings.setdefault(key, set()).add(line)
        for key, lines in wordings.items():
            self.assertEqual(len(lines), 1, key)
        scopes = {generated(name)[generated(name).index("**Scope.**"):].split("\n", 1)[0] for name in PLACEMENT if PLACEMENT[name]}
        self.assertEqual(len(scopes), 1, "the scope and depth line has one wording on every route")

    def test_consumed_clauses_carry_label_meanings(self) -> None:
        d4 = generated("software-implementation")
        for meaning in (
            "none declared: only negligible probes using no shared, metered or queued resource; propose the rest",
            "missing, irrecoverable, archaeology-only or misleading realized records",
            "a null names examined and materially unexamined areas",
            "as a gap, never as none, a null or no selection: findings always;",
            "including when nothing returns",
            "lineage including delegated or resumed work, without double-counting overlapping trials",
            "a recorded finding bearing on it that has not been raised as a Serious Challenge",
            "evidently produced, ran and reviewed no realized results and prepared no gate evidence",
            "known lower bound, unknown interval and claim limit",
            "its home's native asserter",
            "asserter stated in its content as human or AI and which agent",
            "an instruction is not ratification",
            "never technical Review alone",
            "no retention/projection change",
            "An inaccessible or unsearchable home is a named coverage limit, enough by default",
        ):
            self.assertIn(meaning, d4)
        d1 = generated("scientific-formulation")
        for meaning in (
            "applicable, inapplicable with its reason, or review-required",
            "neither changes nor closes the tension's own status",
            "is marked proposed until the revision's acceptance considers it",
            "retention/destructive boundaries",
            "which binds only after the stakeholder or task authority accepts it",
        ):
            self.assertIn(meaning, d1)

    def test_delegate_questions_carry_their_qualifiers_with_one_wording_per_variant(self) -> None:
        blocks: dict[str, str] = {}
        for name in PLACEMENT:
            text = generated(name)
            self.assertEqual(block_problems(name, text), [], name)
            if not PLACEMENT[name]:
                continue
            block = blocks[name] = text[text.index(BLOCK_HEAD):text.index("**Before you finish")]
            self.assertEqual(tuple(key for key in QUESTIONS if key in question_lines(block)),
                             SPECIALIST_QUESTIONS.get(name, QUESTIONS), name)
            self.assertIn("adds nothing except answers its delegator asked for and gaps owed for its delegates", text, name)
            for old in ("On return", "ask for findings or none", "Ask each delegate asked for findings"):
                self.assertNotIn(old, text, name)
        # the delegate parts (everything before the element lead, after the scope line) are one wording per role family
        def delegate_part(name: str) -> str:
            block = blocks[name]
            return block[block.index(DELEGATE_HEAD):]
        self.assertEqual(len({delegate_part(name) for name in ROLES}), 1)
        self.assertEqual(len({delegate_part(name) for name in SPECIALIST_QUESTIONS}), 1)
        self.assertIn("never as none or a null", delegate_part("software-documentation"))
        for name in ROLES:
            self.assertIn("judgments with no reported search", generated(name), name)

    def test_block_checks_reject_a_missing_question_element_or_qualifier(self) -> None:
        d3 = generated("software-design")
        self.assertEqual(block_problems("software-design", d3), [])
        # a missing delegate question
        dropped = "\n".join(line for line in d3.split("\n") if not line.startswith(QUESTION_START["Realized results"]))
        self.assertTrue(any("question Realized results missing" in m for m in block_problems("software-design", dropped)))
        # a missing element
        no_element = "\n".join(line for line in d3.split("\n") if not line.startswith(ELEMENT_PREFIX["3"]))
        self.assertTrue(any("element 3 missing" in m for m in block_problems("software-design", no_element)))
        # a lost qualifier: the launched-work clause, then a question-specific one
        launched = d3.replace("For that judgment, including any tools or agents you launched, what", "For that judgment, what", 1)
        self.assertTrue(any("Tensions question lost its launched-work qualifier" in m for m in block_problems("software-design", launched)))
        reworded = d3.replace("Did your work, including any tools or agents you launched, evaluate", "Did your work evaluate", 1)
        self.assertTrue(any("question Variants missing" in m for m in block_problems("software-design", reworded)))
        for key, qualifiers in QUESTION_QUALIFIERS.items():
            for qualifier in qualifiers:
                broken = d3.replace(qualifier, "", 1)
                self.assertTrue(any(f"{key} question lost its qualifier" in m for m in block_problems("software-design", broken)),
                                f"{key}: {qualifier!r}")
        # the gap rule's exemptions
        gap = d3.replace("unless the task evidently produced, ran and reviewed no realized results and prepared no gate evidence", "", 1)
        self.assertTrue(any("gap rule lost" in m for m in block_problems("software-design", gap)))
        # a route that must not carry a question or element
        doc = generated("software-documentation")
        extra = doc.replace(QUESTION_START["Realized results"], QUESTION_START["Variants"] + " x " + QUESTION_START["Realized results"], 1)
        self.assertTrue(any("must not be carried" in m for m in block_problems("software-documentation", extra)))
        hygiene = generated("repository-hygiene") + "\n" + BLOCK_HEAD + "\n"
        self.assertTrue(block_problems("repository-hygiene", hygiene))
        # a removed section
        self.assertTrue(block_problems("software-design", d3[:d3.index(BLOCK_HEAD)]))

    def test_selection_description_covers_new_classes_without_narrowing(self) -> None:
        front = entrypoint("software-implementation").read_text(encoding="utf-8").split("---", 2)[1]
        description = next(line for line in front.splitlines() if line.startswith("description: "))
        for phrase in ("scientific/technical", "run or analyze", "review scientific results", "gate evidence",
                       "copy, transcribe or relay scientific results", "delegate any of this work"):
            self.assertIn(phrase, description)

    def test_no_accepted_66_entrypoint_text_removed_and_kernel_unchanged(self) -> None:
        kernel = accepted("source/shared/references/abstraction-and-concretization.md")
        if kernel is None:
            self.skipTest("accepted 6.6 ref unavailable in this clone")
        self.assertEqual((REFS / "abstraction-and-concretization.md").read_text(encoding="utf-8"), kernel)
        for name in PLACEMENT:
            kind = "roles" if name in ROLES else "specialists"
            base = accepted(f"source/{kind}/{name}/SKILL.md")
            current = entrypoint(name).read_text(encoding="utf-8").splitlines()
            for line in base.splitlines():
                if name == "software-implementation" and line.startswith("description: "):
                    continue
                self.assertIn(line, current, f"{name}: removed or reworded 6.6 line {line[:60]!r}")

    def test_refines_deltas_and_routes_are_present(self) -> None:
        expected = {
            REFS / "scientific-formulation.md": "## Scientific inspectability need (O1)",
            REFS / "numerical-algorithm-design.md": "## Numerical inspectability need (O1)",
            REFS / "architecture-and-design.md": "## Realized-record architecture (O1)",
            REFS / "evidence-evolution-and-dependencies.md": "**inquiry status**",
            REFS / "scientific-technical-writing.md": "**Reporting roles.**",
            REFS / "workflow-and-workplans.md": "**Gate evidence (Channel C).**",
            TEMPLATES / "abstraction_concretization_change_plan_template.md": "## 3b. Revision tension record",
            TEMPLATES / "implementation_workplan_template.md": "## 1a. Scientific inspectability (O1)",
        }
        for path, marker in expected.items():
            self.assertIn(marker, path.read_text(encoding="utf-8"), path.name)
        workflow = (REFS / "workflow-and-workplans.md").read_text(encoding="utf-8")
        self.assertIn("**Bidirectional scientific Review.**", workflow)
        self.assertIn("**Product-scope acceptance.**", workflow)
        for routed in ("storage-and-io.md", "configuration-and-policy.md", "testing-and-validation.md",
                       "security-and-trust-boundaries.md", "concurrency-and-orchestration.md"):
            self.assertIn(f"]({OWNER})", (REFS / routed).read_text(encoding="utf-8"), routed)

    def test_owner_does_not_restate_routed_contracts(self) -> None:
        owner = (REFS / OWNER).read_text(encoding="utf-8")
        gate = owner.split("## Human gate evidence", 1)[1].split("\n## ", 1)[0]
        self.assertIn("owned by the [workflow](workflow-and-workplans.md) owner", gate)
        self.assertLess(len(gate), 400)
        self.assertIsNone(re.search(r"(?m)^\*\*evidence specification\*\*", owner))

    def test_versioning_owner_lists_frozen_66_and_new_70_profiles(self) -> None:
        text = (REFS / "protocol-versioning-and-compatibility.md").read_text(encoding="utf-8")
        self.assertIn("`ssdp-protocol-6.6`", text)
        self.assertIn("`ssdp-protocol-7.0`", text)
        self.assertIn("`ssdp-protocol-7.1`", text)
        self.assertIn("`ssdp-protocol-7.2`", text)


if __name__ == "__main__":
    unittest.main()
