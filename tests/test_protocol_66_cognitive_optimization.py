"""Protocol 6.6 structural qualification.

These oracles establish only structural/routing/tooling properties (kernel scope,
owner preservation, activation vs transport, selection-metadata hygiene, version
preflight behavior). Semantic adequacy of the assembled prose still requires
independent Review; live selection/trajectory claims require the Stage F evidence.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
REFS = SOURCE / "shared" / "references"
sys.path.insert(0, str(SOURCE))
sys.path.insert(0, str(ROOT / "qualification" / "ssdp66" / "eval"))
import project_engineering_memory as pem  # noqa: E402
import validate_packages  # noqa: E402
import version_preflight  # noqa: E402

BASELINE_SOURCE = "7f7b5e24858e813e45ace867a7f8ea5180f43bf0"
ROLES = ("scientific-formulation", "numerical-algorithm-design", "software-design", "software-implementation")
SPECIALISTS = ("software-documentation", "software-maintenance-audit", "repository-hygiene")
LINK_RE = re.compile(r"\]\((references|templates)/([A-Za-z0-9_.-]+\.md)\)")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def skill(name: str) -> str:
    kind = "roles" if name in ROLES else "specialists"
    return read(f"source/{kind}/{name}/SKILL.md")


def mandatory_sentence(text: str) -> str:
    for para in text.split("\n\n"):
        flat = " ".join(para.split())
        if flat.startswith("Before substantive"):
            return para
    raise AssertionError("entrypoint has no unconditional pre-reasoning read sentence")


def git_show(ref: str, rel: str) -> str | None:
    proc = subprocess.run(["git", "-C", str(ROOT), "show", f"{ref}:{rel}"], capture_output=True)
    return proc.stdout.decode("utf-8") if proc.returncode == 0 else None


def sentences(text: str) -> list[str]:
    flat = " ".join(text.split())
    return [s.strip() for s in re.split(r"(?<=[.;:])\s+(?=[A-Z`])", flat) if len(s.strip()) > 40]


class KernelAndOwnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.kernel = read("source/shared/references/abstraction-and-concretization.md")
        self.semantic = read("source/shared/references/semantic-definition-and-traceability.md")

    def test_kernel_keeps_universal_invariants(self) -> None:
        for phrase in (
            "semantics(K) |= I(A1) AND ... AND I(An) AND C",
            "minimum justified concretization complexity",
            "is **material** when",
            "concretization fidelity",
            "abstraction adequacy",
            "SERIOUS CHALLENGE",
            "risk override",
            "not a fifth authority domain",
            "infer_C(x) -> context_available_C(x) -> source_available_D(x)",
            "inert data",
            "Lossless Representation Rule",
            "stop when it cannot",
        ):
            self.assertIn(phrase, self.kernel)

    def test_kernel_excludes_conditional_detail(self) -> None:
        for detail in (
            "`FOUNDATIONAL_ASSUMED`",
            "strongly connected component",
            "`PRIMITIVE`",
            "memory_schema_version",
            "stale-dependent",
            "history/SEMANTIC_EVOLUTION.md",
            "`HOT`",
        ):
            self.assertNotIn(detail, self.kernel)
        self.assertIn("(semantic-definition-and-traceability.md)", self.kernel)
        self.assertIn("(workflow-and-workplans.md)", self.kernel)

    def test_kernel_is_materially_smaller_than_accepted_65(self) -> None:
        baseline = git_show(BASELINE_SOURCE, "source/shared/references/abstraction-and-concretization.md")
        if baseline is None:
            self.skipTest("accepted 6.5 source is not resolvable in this clone")
        self.assertLess(len(self.kernel.encode()), 0.7 * len(baseline.encode()))

    def test_every_65_semantic_definition_sentence_survives_at_a_current_owner(self) -> None:
        baseline = git_show(BASELINE_SOURCE, "source/shared/references/abstraction-and-concretization.md")
        if baseline is None:
            self.skipTest("accepted 6.5 source is not resolvable in this clone")
        section = baseline.split("## Semantic-definition and traceability discipline", 1)[1].split("## Universal invariant", 1)[0]
        current = " ".join((self.semantic + "\n" + self.kernel).split())
        missing = [s for s in sentences(section) if s not in current]
        self.assertEqual(missing, [])

    def test_every_65_lifecycle_and_mutation_sentence_survives_at_a_current_owner(self) -> None:
        baseline = git_show(BASELINE_SOURCE, "source/shared/references/abstraction-and-concretization.md")
        if baseline is None:
            self.skipTest("accepted 6.5 source is not resolvable in this clone")
        section = baseline.split("Projects may encode lifecycle locally", 1)[1].split("For high-risk scientific/numerical claims", 1)[0]
        current = " ".join((read("source/shared/references/workflow-and-workplans.md") + "\n" + self.kernel).split())
        missing = [s for s in sentences("Projects may encode lifecycle locally" + section) if s not in current]
        self.assertEqual(missing, [])

    def test_semantic_owner_has_risk_triggered_router_without_weakening_availability(self) -> None:
        self.assertIn("ordinary engineering meaning", self.semantic)
        self.assertIn("Activation controls when this detail is loaded, not whether", self.semantic)
        self.assertIn("A discoverable route establishes source availability, not runtime context availability", self.semantic)
        self.assertIn("`subject -> prerequisite`", self.semantic)


class ActivationTransportDiscoveryTests(unittest.TestCase):
    def test_roles_route_semantic_owner_conditionally_not_eagerly(self) -> None:
        for role in ROLES:
            text = skill(role)
            with self.subTest(role=role):
                self.assertIn("references/semantic-definition-and-traceability.md", text)
                self.assertNotIn("semantic-definition-and-traceability.md", mandatory_sentence(text))
                self.assertNotIn("project-engineering-memory.md", mandatory_sentence(text))
                self.assertNotIn("workflow-and-workplans.md", mandatory_sentence(text))

    def test_pem_schema_is_transported_but_never_root_activated(self) -> None:
        owner = read("source/shared/references/project-engineering-memory.md")
        self.assertIn("(project-engineering-memory-schema.md)", owner)
        for name in (*ROLES, *SPECIALISTS):
            with self.subTest(skill=name):
                self.assertNotIn("project-engineering-memory-schema.md", skill(name))
                packaged = ROOT / "dist" / "skills" / name / "references"
                if (packaged / "project-engineering-memory.md").is_file():
                    self.assertTrue((packaged / "project-engineering-memory-schema.md").is_file())

    def test_semantic_owner_is_transported_to_every_role_package(self) -> None:
        for role in ROLES:
            self.assertTrue((ROOT / "dist" / "skills" / role / "references" / "semantic-definition-and-traceability.md").is_file(), role)

    def test_package_membership_exceeds_declared_activation(self) -> None:
        text = skill("software-implementation")
        packaged = {p.name for p in (ROOT / "dist/skills/software-implementation/references").glob("*.md")}
        mandatory = {m.group(2) for m in LINK_RE.finditer(mandatory_sentence(text))}
        self.assertEqual(mandatory, {"abstraction-and-concretization.md", "specification-and-implementation.md"})
        self.assertGreater(len(packaged), 3 * len(mandatory))
        self.assertIn("package membership are not activation commands", text)

    def test_frozen_routes_fire_reachably_and_forbid_eager_loading(self) -> None:
        import harness  # qualification/ssdp66/eval

        report = harness.static_report(None)
        for route_id, route in report["routes"].items():
            with self.subTest(route=route_id):
                self.assertEqual(route["unreachable_fired_concerns"], [])
                self.assertEqual(route["eager_forbidden_concerns"], [])

    def test_ordinary_route_mandatory_closure_is_smaller_than_65_baseline(self) -> None:
        import harness

        baseline = json.loads((ROOT / "qualification/ssdp66/eval/results/static-baseline-6.5.json").read_text(encoding="utf-8"))
        current = harness.static_report(None)
        for route_id in ("R1-local-d4-repair", "R4-d2-specialized-import"):
            with self.subTest(route=route_id):
                self.assertLess(current["routes"][route_id]["mandatory_closure"]["bytes"],
                                0.85 * baseline["routes"][route_id]["mandatory_closure"]["bytes"])
        self.assertLess(current["routes"]["R3-d3-mature-replacement"]["route_closure"]["bytes"],
                        baseline["routes"]["R3-d3-mature-replacement"]["route_closure"]["bytes"])


class SelectionMetadataTests(unittest.TestCase):
    def test_descriptions_are_selection_interfaces_without_release_state(self) -> None:
        for name in (*ROLES, *SPECIALISTS):
            frontmatter, _ = validate_packages.parse_frontmatter(skill(name))
            description = frontmatter["description"]
            with self.subTest(skill=name):
                self.assertLessEqual(len(description), 600)
                self.assertIsNone(re.search(r"\b\d+\.\d+(?:\.\d+)?\b", description))
                self.assertIsNone(re.search(r"\b[0-9a-f]{40}\b", description))
                for token in ("accepted-current", "Protocol 6", "USES_DEFINITION", "HAS", "PEM"):
                    self.assertNotIn(token, description)
                self.assertRegex(description, r"\bUse (to|for|after)\b")
                self.assertRegex(description, r"\b(Not for|Routes|does not)\b")

    def test_every_entrypoint_opens_with_a_build_stamped_version_check(self) -> None:
        version = (SOURCE / "PROTOCOL_VERSION").read_text(encoding="utf-8").strip()
        for name in (*ROLES, *SPECIALISTS):
            text = skill(name)
            with self.subTest(skill=name):
                head, _, _ = text.partition("## Routing")
                self.assertIn("**Version entry check.** This package is SSDP `REPLACE_WITH_SKILL_PROTOCOL_VERSION`", head)
                self.assertIn("references/protocol-versioning-and-compatibility.md", head)
                built = (ROOT / "dist" / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(f"This package is SSDP `{version}`", built)
                self.assertNotIn("REPLACE_WITH_SKILL_PROTOCOL_VERSION", built)

    def test_generic_core_validity_does_not_require_vendor_adapter(self) -> None:
        name = "software-implementation"
        root = ROOT / "dist" / "skills" / name
        files = validate_packages.directory_files(root)
        files.pop("agents/openai.yaml")
        self.assertEqual(validate_packages.validate_core_bundle(files, name, "role", SOURCE / "roles" / name), [])
        self.assertEqual(validate_packages.validate_openai_adapter(files, SOURCE / "roles" / name), ["OpenAI adapter missing agents/openai.yaml"])


class WorkingStateAndMemoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = read("source/shared/references/workflow-and-workplans.md")
        self.pem = read("source/shared/references/project-engineering-memory.md")

    def test_working_state_is_derived_optional_and_stale_on_basis_change(self) -> None:
        for phrase in (
            "derived coordination state, not authority",
            "cannot create or mutate D1-D4 authority, declare acceptance or Review outcome",
            "never a required repository artifact for local work",
            "no schema, file, tool or Orchestrator is required",
            "it is stale and must be re-derived from canonical owners",
            "Dropping an open blocker, required check, uncertainty or reopen condition is a Lossless Representation defect",
        ):
            self.assertIn(phrase, self.workflow)
        self.assertEqual(sorted(p.name for p in SOURCE.rglob("*working*state*")), [])

    def test_transient_progress_does_not_mutate_workplan_contract(self) -> None:
        self.assertIn("### Workplan contract versus transient progress", self.workflow)
        self.assertIn("Do not amend it merely because a task completed", self.workflow)

    def test_agent_facing_pem_is_compact_and_schema_stays_cold(self) -> None:
        self.assertLess(len(self.pem.encode()), 12_000)
        for schema_only in ("recurrence_basis", "temperature_override", "maturity_basis", "pem-repair-acceptance"):
            self.assertNotIn(schema_only, self.pem)
        block = re.search(r"```yaml\n(pem_basis:.*?)```", self.pem, re.S)
        self.assertIsNotNone(block)
        self.assertEqual(set(yaml.safe_load(block.group(1))["pem_basis"]), pem.HAS_BASIS_FIELDS)
        for protection in (
            "Missing memory is not absence",
            "Applicability is **not** restricted to the active summary or `HOT` entries",
            "Query/index/summary output is a derived view, never canonical memory",
            "treat an unhealthy/unavailable binding as `REVIEW_REQUIRED`",
            "Keep neutral/contradicting/inconclusive evidence",
            "A first clean local defect",
        ):
            self.assertIn(protection, self.pem)

    def test_duplicate_pem_procedures_route_to_the_single_owner(self) -> None:
        for rel in ("source/shared/references/workflow-and-workplans.md", "source/shared/references/repository-intake.md"):
            text = read(rel)
            with self.subTest(rel=rel):
                self.assertIn("(project-engineering-memory.md)", text)
                self.assertNotIn("candidate_overlay_semantic_candidate", text)


class CognitiveRoutingTests(unittest.TestCase):
    def test_cognitive_escalation_is_vendor_neutral_execution_policy(self) -> None:
        convergence = read("source/shared/references/convergence-and-cycle-economy.md")
        for phrase in (
            "least expensive cognitive configuration",
            "do not duplicate trustworthy host automatic resource routing",
            "never authority or a pass threshold",
            "a stronger model does not substitute for independently required Review",
            "a high-stakes parent does not force the strongest configuration onto every child detail",
        ):
            self.assertIn(phrase, convergence)
        for path in [*REFS.glob("*.md"), *SOURCE.glob("*/*/SKILL.md")]:
            self.assertIsNone(re.search(r"(?i)\b(gpt|claude|sonnet|opus|gemini)\b", path.read_text(encoding="utf-8")), path.name)

    def test_independent_trajectories_are_optional_and_common_mode_bounded(self) -> None:
        workflow = read("source/shared/references/workflow-and-workplans.md")
        for phrase in (
            "Multi-agent execution is never required",
            "A subagent that receives the author's conclusions is not independent",
            "not epistemic independence",
            "cannot erase unresolved contradictory material evidence by vote",
        ):
            self.assertIn(phrase, workflow)

    def test_review_strategy_switches_after_related_recurrence(self) -> None:
        convergence = read("source/shared/references/convergence-and-cycle-economy.md")
        self.assertIn("### Review strategy after recurrence", convergence)
        self.assertIn("No numeric review count changes the pass threshold", convergence)
        self.assertIn("recurrence does not automatically force redesign", convergence)


class VersionPreflightTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.skill = self.tmp / "skill"
        self.skill.mkdir()
        (self.skill / "PROTOCOL_VERSION").write_text("6.6.0\n", encoding="utf-8")
        (self.skill / "protocol-manifest.json").write_text(json.dumps({"protocol_version": "6.6.0"}), encoding="utf-8")
        self.state = ROOT / "PROTOCOL-RELEASE-STATE.yaml"

    def plan(self, version: str | None) -> Path:
        path = self.tmp / "wp.md"
        head = f"protocol_version: {version}\n" if version else "kind: note\n"
        path.write_text(f"---\n{head}---\n\n# Plan\n", encoding="utf-8")
        return path

    def test_matching_version_continues(self) -> None:
        result = version_preflight.preflight(self.skill, version_preflight.workplan_version(self.plan("6.6.0")), self.state)
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(version_preflight.preflight(self.skill, "6.6", self.state)["decision"], "CONTINUE")

    def test_frozen_historical_work_resolves_its_exact_source_not_latest(self) -> None:
        result = version_preflight.preflight(self.skill, version_preflight.workplan_version(self.plan("6.4.0")), self.state)
        self.assertEqual(result["decision"], "RESOLVE_COMPATIBLE_SOURCE")
        self.assertEqual(result["public_source_ref"], "e09a9d1480211eea2d16d722182bb5c6de1bee12")

    def test_mismatch_without_mapping_is_truthful_nonclosure(self) -> None:
        self.assertEqual(version_preflight.preflight(self.skill, "6.4.0", None)["decision"], "UNRESOLVED")
        self.assertEqual(version_preflight.preflight(self.skill, "5.16.0", self.state)["decision"], "UNRESOLVED")
        self.assertEqual(version_preflight.preflight(self.skill, "main", self.state)["decision"], "UNRESOLVED")

    def test_unversioned_task_needs_no_lookup(self) -> None:
        result = version_preflight.preflight(self.skill, version_preflight.workplan_version(self.plan(None)), None)
        self.assertEqual(result["decision"], "UNVERSIONED_CONTINUE")

    def test_incoherent_package_identity_is_reported(self) -> None:
        (self.skill / "protocol-manifest.json").write_text(json.dumps({"protocol_version": "6.5.0"}), encoding="utf-8")
        self.assertEqual(version_preflight.preflight(self.skill, "6.6.0", self.state)["decision"], "PACKAGE_INCOHERENT")

    def test_governing_workplan_of_this_cycle_is_detected_as_65_bound(self) -> None:
        governing = version_preflight.workplan_version(ROOT / "workplans/active/SSDP-6.6-COGNITIVE-OPERATIONAL-OPTIMIZATION.md")
        self.assertEqual(governing, "6.5.0")
        result = version_preflight.preflight(self.skill, governing, self.state)
        self.assertEqual(result["decision"], "RESOLVE_COMPATIBLE_SOURCE")
        self.assertEqual(result["public_source_ref"], "7f7b5e24858e813e45ace867a7f8ea5180f43bf0")


if __name__ == "__main__":
    unittest.main()
