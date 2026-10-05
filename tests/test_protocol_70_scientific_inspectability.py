"""Protocol 7.0 structural qualification (workplan section 11.5 structural checks).

These checks are necessary, not sufficient: they cannot show that agents behave as the
doctrine requires. Live behavior is qualified separately under the frozen Protocol 7
qualification contract.
"""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
REFS = SOURCE / "shared" / "references"
TEMPLATES = SOURCE / "shared" / "templates"
OWNER = "scientific-inspectability-and-initiative.md"
ACCEPTED_66 = "22f4bdba53795da3a6f13f162529f3a843fc37ae"

ROLES = ("scientific-formulation", "numerical-algorithm-design", "software-design", "software-implementation")
SPECIALISTS = ("software-documentation", "software-maintenance-audit", "repository-hygiene")
ELEMENT_PREFIX = {
    "1": "1. Within the task's declared resource budget",
    "2": "2. For a selected reported/delivered survivor",
    "3": "3. Before relying on accepted D1/D2 authority for a consequential judgment",
    "4": "4. Keep claims within evidence",
    "5": "5. When revising, renaming, splitting, merging or replacing D1/D2 authority",
    "6": "6. For a built/changed scientific pipeline, analysis or report",
    "7": "7. When authoring or materially revising D1/D2/D3 authority for such software",
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
TRIGGER = "> **Owner-load trigger.** Load the scientific-inspectability owner before a consequential scientific analysis"
DELEGATE_HEAD = "**When you delegate.**"
COMPLETION_HEAD = "## Scientific completion when the predicate above applies"
LAUNCHED = "any tools or agents you launched"
QUESTIONS = ("Findings", "Realized results", "Variants", "Tensions")
SPECIALIST_QUESTIONS = {"software-documentation": QUESTIONS[:2], "software-maintenance-audit": QUESTIONS[:2]}


def entrypoint(name: str) -> Path:
    kind = "roles" if name in ROLES else "specialists"
    return SOURCE / kind / name / "SKILL.md"


def element_lines(text: str) -> dict[str, str]:
    found = {}
    for key, prefix in ELEMENT_PREFIX.items():
        lines = [line for line in text.splitlines() if line.startswith(prefix)]
        if lines:
            found[key] = lines[0]
    return found


def delegate_block(text: str) -> str:
    """The delegate-request block: from its lead line to the first numbered element."""
    start = text.index(DELEGATE_HEAD)
    return text[start:text.index("\n\n1. ", start)]


def question_lines(block: str) -> dict[str, str]:
    return {key: line for key in QUESTIONS for line in block.splitlines() if line.startswith(f"- **{key}")}


def accepted(rel: str) -> str | None:
    proc = subprocess.run(["git", "-C", str(ROOT), "show", f"{ACCEPTED_66}:{rel}"], capture_output=True)
    return proc.stdout.decode("utf-8") if proc.returncode == 0 else None


class Protocol70StructuralTests(unittest.TestCase):
    def test_single_canonical_owner_carries_frozen_predicate_and_trigger(self) -> None:
        owners = [path.name for path in REFS.glob("*.md") if "Obligation predicate." in path.read_text(encoding="utf-8")]
        self.assertEqual(owners, [OWNER])
        owner = (REFS / OWNER).read_text(encoding="utf-8")
        self.assertIn(PREDICATE, owner)
        self.assertIn(TRIGGER, owner)
        for bound in (
            "not guaranteed to perform a tension search",
            "reported as given",
            "may escape rename-following history",
            "without verifying claimed authority",
            "non-writing fallback",
        ):
            self.assertIn(bound, owner)

    def test_routing_line_and_elements_are_placed_exactly(self) -> None:
        for name, expected in PLACEMENT.items():
            text = entrypoint(name).read_text(encoding="utf-8")
            self.assertEqual(set(element_lines(text)), expected, name)
            self.assertEqual(ROUTE_MARK in text, bool(expected), name)
            if expected:
                self.assertEqual(text.count("## Scientific completion when the predicate above applies"), 1, name)
                self.assertLess(text.index(ROUTE_MARK), text.index("## Scientific completion"), name)

    def test_each_element_has_one_wording_across_entrypoints(self) -> None:
        wordings: dict[str, set[str]] = {}
        for name in PLACEMENT:
            for key, line in element_lines(entrypoint(name).read_text(encoding="utf-8")).items():
                wordings.setdefault(key, set()).add(line)
        routes = {
            line.removeprefix("- ")
            for name in PLACEMENT
            for line in entrypoint(name).read_text(encoding="utf-8").splitlines()
            if ROUTE_MARK in line
        }
        self.assertEqual(len(routes), 1)
        for key, lines in wordings.items():
            self.assertEqual(len(lines), 1, key)

    def test_consumed_clauses_carry_label_meanings(self) -> None:
        d4 = entrypoint("software-implementation").read_text(encoding="utf-8")
        for meaning in (
            "if none, only negligible probes using no shared, metered or queued resource; propose the rest",
            "missing, irrecoverable, archaeology-only or misleading realized records",
            "a null states examined and materially unexamined areas",
            "as a gap, never as none, a null or no selection: findings always;",
            "including when it returns nothing",
            "lineage including delegated or resumed work, without double-counting overlapping trials",
            "a recorded finding bearing on it that has not been raised as a Serious Challenge",
            "evidently produced, ran and reviewed no realized results and prepared no gate evidence",
            "known lower bound, unknown interval and claim limit",
            "natively attributed account/record asserter",
            "content-stated human/AI asserter and which agent",
            "an instruction is not ratification",
            "never technical Review alone",
            "no retention/projection change",
        ):
            self.assertIn(meaning, d4)
        d1 = entrypoint("scientific-formulation").read_text(encoding="utf-8")
        for meaning in (
            "applicable, inapplicable with its reason, or review-required",
            "neither changes nor closes the tension's own status",
            "is marked proposed until the revision's acceptance considers it",
            "retention/destructive boundaries",
            "which binds only after the stakeholder or task authority accepts it",
        ):
            self.assertIn(meaning, d1)

    def test_delegate_request_block_is_relocated_once_with_one_wording_per_variant(self) -> None:
        blocks: dict[str, str] = {}
        for name in PLACEMENT:
            text = entrypoint(name).read_text(encoding="utf-8")
            if name == "repository-hygiene":
                self.assertNotIn(DELEGATE_HEAD, text, name)
                continue
            self.assertEqual(text.count(DELEGATE_HEAD), 1, name)
            completion = text.index(COMPLETION_HEAD)
            self.assertLess(completion, text.index(DELEGATE_HEAD), name)
            self.assertLess(text.index(DELEGATE_HEAD), text.index("\n\n1. Within the task's declared resource budget"), name)
            block = blocks[name] = delegate_block(text)
            expected = SPECIALIST_QUESTIONS.get(name, QUESTIONS)
            found = question_lines(block)
            self.assertEqual(tuple(found), expected, name)
            for key, line in found.items():
                self.assertIn(LAUNCHED, line, f"{name}: {key} question lost its launched-work qualifier")
            for dropped in set(QUESTIONS) - set(expected):
                self.assertNotIn(f"- **{dropped}", block, name)
            self.assertIn("including when it returns nothing", block, name)
            self.assertNotIn("On return", block, name)
            self.assertIn("findings always;", block, name)
            self.assertIn("evidently produced, ran and reviewed no realized results", block, name)
            # relocated, not duplicated: the old delegate-request sentences are gone from the element prose
            for old in ("ask for findings or none", "Ask each delegate asked for findings", "Ask a delegate relying on it",
                        "Unanswered findings are always a gap"):
                self.assertNotIn(old, text, f"{name}: old sentence {old!r} still present")
            # the delegator's own duties stay in the element prose
            self.assertIn("adds nothing except asked delegate answers/gaps", text, name)
        roles = {blocks[name] for name in ROLES}
        self.assertEqual(len(roles), 1, "the role entrypoints must carry one block wording")
        specialists = {blocks[name] for name in SPECIALIST_QUESTIONS}
        self.assertEqual(len(specialists), 1, "the specialists must carry one block wording")
        role_block, specialist_block = next(iter(roles)), next(iter(specialists))
        shared = role_block[:role_block.index("- **Variants")]
        self.assertTrue(specialist_block.startswith(shared), "specialist lead line and first two questions must equal the role block's")
        self.assertIn("variants, for a returned result, with unknown selection history and claim limit", role_block)
        self.assertNotIn("variant", specialist_block.split("- **Realized results")[1])
        self.assertIn("never as none or a null", specialist_block)
        for name in ROLES:
            self.assertIn("judgments with no reported search", entrypoint(name).read_text(encoding="utf-8"), name)

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


if __name__ == "__main__":
    unittest.main()
