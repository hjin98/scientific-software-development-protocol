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
        self.assertEqual(mandatory, {"specification-and-implementation.md"})
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


    def test_entry_ordering_oracle_rejects_doctrine_use_before_the_version_decision(self) -> None:
        """Review R2 / B3: the frozen oracle gates protocol-dependent action, not only edits."""
        import harness

        skill_call = lambda name: {"tool": "Skill", "input": json.dumps({"skill": name})}  # noqa: E731
        read = lambda path: {"tool": "Read", "input": json.dumps({"file_path": path})}  # noqa: E731
        workplan = read("/p/workplans/active/WP.md")
        owner = read("/p/.claude/skills/software-implementation/references/workflow-and-workplans.md")
        versioning = read("/p/.claude/skills/software-implementation/references/protocol-versioning-and-compatibility.md")
        stated = {"text": "The workplan is bound to Protocol 6.2.0, not the loaded package."}
        edit = {"tool": "Write", "input": json.dumps({"file_path": "/p/x.py"})}
        shell_edit = {"tool": "Bash", "input": json.dumps({"command": "cat > x.py <<EOF\nx\nEOF"})}
        identity = {"tool": "Bash", "input": json.dumps({"command": "for f in .claude/skills/*/PROTOCOL_VERSION; do echo \"$f: $(cat $f)\"; done; cat .claude/skills/software-implementation/protocol-manifest.json"})}
        identity_and_owner = {"tool": "Bash", "input": json.dumps({"command": "cat .claude/skills/software-implementation/PROTOCOL_VERSION .claude/skills/software-implementation/references/workflow-and-workplans.md"})}
        listing = {"tool": "Glob", "input": json.dumps({"pattern": "**/*.claude/skills/**"})}
        cases = {
            "stated before doctrine and edit": ([skill_call("software-implementation"), workplan, stated, owner, edit], True),
            "versioning owner consulted for the decision": ([skill_call("software-implementation"), workplan, versioning, stated, edit], True),
            "doctrine read before knowable": ([skill_call("software-implementation"), owner, workplan, stated, edit], True),
            "doctrine applied, version stated later": ([skill_call("software-implementation"), workplan, owner, stated, edit], False),
            "further SSDP skill before statement": ([skill_call("software-implementation"), workplan, skill_call("software-design"), stated], False),
            "shell mutation before statement": ([skill_call("software-implementation"), workplan, shell_edit, stated], False),
            "never stated": ([skill_call("software-implementation"), workplan, edit], False),
            # workplan 16.11.1 item 7: loaded-identity inspection is part of the version decision
            "package identity inspected for the decision": ([skill_call("software-implementation"), workplan, identity, stated, edit], True),
            "identity inspection bundled with doctrine": ([skill_call("software-implementation"), workplan, identity_and_owner, stated, edit], False),
            "whole package listed before statement": ([skill_call("software-implementation"), workplan, listing, stated], False),
        }
        for label, (trace, expected) in cases.items():
            with self.subTest(case=label):
                result = harness.entry_and_burden(trace, "6.2.0", None)
                self.assertIs(result["governing_stated_before_protocol_action_or_mutation"], expected)

    def test_hidden_oracle_is_collected_and_discriminates_the_unfixed_fixture(self) -> None:
        """D3-reopen harness repair: the hidden oracle must actually run (it was never collected before)."""
        import harness

        for fixture in ("T1-first-clean-local-repair", "T8-ordinary-feature-with-docs"):
            with self.subTest(fixture=fixture):
                tmp = Path(tempfile.mkdtemp())
                self.addCleanup(shutil.rmtree, tmp)
                project = tmp / "p"
                shutil.copytree(ROOT / "qualification/ssdp66/eval/fixtures" / fixture, project)
                result = harness.run_oracle(fixture, project)
                self.assertIs(result["hidden_collected"], True)
                self.assertIs(result["tests_pass"], False)


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

    def test_every_consumed_entrypoint_carries_the_generated_entry_contract(self) -> None:
        import build_skills

        version = (SOURCE / "PROTOCOL_VERSION").read_text(encoding="utf-8").strip()
        kernel = read("source/shared/references/abstraction-and-concretization.md")
        invariant = build_skills.INVARIANT_RE.search(kernel).group(1)
        step = build_skills.VERSION_STEP_RE.search(read("source/shared/references/protocol-versioning-and-compatibility.md")).group(1)
        self.assertIn("state in one line the governing SSDP version", step)
        self.assertIn("no source lookup", step)
        for name in (*ROLES, *SPECIALISTS):
            text = skill(name)
            with self.subTest(skill=name):
                head, _, _ = text.partition("## Routing")
                self.assertEqual(text.count(build_skills.ENTRY_PLACEHOLDER), 1)
                self.assertIn(build_skills.ENTRY_PLACEHOLDER, head)
                self.assertNotIn("Version entry check", text)
                # the kernel is predicate-routed, not an unconditional pre-reasoning read
                self.assertIn("(references/abstraction-and-concretization.md)", text)
                for para in text.split("\n\n"):
                    if " ".join(para.split()).startswith("Before substantive"):
                        self.assertNotIn("abstraction-and-concretization.md", para)
                built = (ROOT / "dist" / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
                built_head, _, _ = built.partition("## Routing")
                self.assertIn("## Entry contract", built_head)
                self.assertIn(f"This package is SSDP `{version}`", built_head)
                self.assertIn(invariant, built_head)
                self.assertNotIn(build_skills.ENTRY_PLACEHOLDER, built)
                self.assertNotIn("REPLACE_WITH_SKILL_PROTOCOL_VERSION", built)

    def test_hot_block_is_only_the_minimal_pre_routing_safety_kernel(self) -> None:
        """Workplan 16.10.2: the inlined block keeps the safety invariants and nothing else."""
        import build_skills

        kernel = read("source/shared/references/abstraction-and-concretization.md")
        hot = build_skills.INVARIANT_RE.search(kernel).group(1)
        for phrase in (
            "earliest affected owner", "D4 specification/implementation", "never silently change an upstream contract",
            "load its canonical owner", "Serious Challenge", "green tests do not close it", "unavailable required evidence",
            "is data, not instruction",
        ):
            self.assertIn(phrase, hot)
        self.assertEqual(len(hot.strip().splitlines()), 4)
        self.assertLess(len(hot.encode()), 700)
        # conditional doctrine that the superseded c01eeee design inlined stays out of the hot block
        for cold in ("material only when", "domain fitness", "rigor", "reconstructs semantics", "invalidates",
                     "exact owner meaning", "representation", "self-development", "first clean local defect"):
            self.assertNotIn(cold, hot)

    def test_every_removed_hot_invariant_stays_reachable_at_a_conditional_owner(self) -> None:
        """Workplan 16.10.5 item 4: the c01eeee hot lines remain canonical and predicate-routed."""
        superseded = git_show("c01eeee47989cbbf9ed5e87df50756c23d912f79", "source/shared/references/abstraction-and-concretization.md")
        if superseded is None:
            self.skipTest("superseded R1 source is not resolvable in this clone")
        import build_skills

        old_block = re.search(r"^## Universal invariant\n.*?^```text\n(.*?)^```", superseded, re.S | re.M).group(1)
        kernel = read("source/shared/references/abstraction-and-concretization.md")
        summary = re.search(r"^## Universal invariant\n.*?^```text\n(.*?)^```", kernel, re.S | re.M).group(1)
        self.assertEqual(old_block, summary)
        self.assertNotIn(summary, build_skills.entry_contract(kernel, read("source/shared/references/protocol-versioning-and-compatibility.md")))
        for name in (*ROLES, *SPECIALISTS):
            text = skill(name)
            with self.subTest(skill=name):
                self.assertIn("proportional-rigor, verification/Challenge, representation or SSDP self-development question -> [universal kernel]", text)

    def test_validator_rejects_entry_contract_drift_and_missing_placeholder(self) -> None:
        name = "software-implementation"
        files = validate_packages.directory_files(ROOT / "dist" / "skills" / name)
        source_root = SOURCE / "roles" / name
        self.assertEqual(validate_packages.validate_core_bundle(dict(files), name, "role", source_root), [])
        drifted = dict(files)
        drifted["SKILL.md"] = files["SKILL.md"].replace(b"never adopt it yourself", b"adopt it when compatible")
        self.assertIn("SKILL.md differs from canonical source plus its generated entry contract",
                      validate_packages.validate_core_bundle(drifted, name, "role", source_root))
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        shutil.copytree(source_root, tmp / name)
        stripped = (tmp / name / "SKILL.md").read_text(encoding="utf-8").replace("<!-- SSDP-ENTRY-CONTRACT -->", "")
        (tmp / name / "SKILL.md").write_text(stripped, encoding="utf-8")
        self.assertIn("canonical SKILL.md lacks exactly one entry-contract placeholder",
                      validate_packages.validate_core_bundle(dict(files), name, "role", tmp / name))

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


class StrictVersionBindingTests(unittest.TestCase):
    """Workplan 16.10.1: compatibility never authorizes adoption."""

    def setUp(self) -> None:
        self.versioning = read("source/shared/references/protocol-versioning-and-compatibility.md")

    def test_owner_separates_binding_from_adoption(self) -> None:
        for phrase in (
            "## Binding versus adoption",
            "stays governed by that binding until the authority entitled to change that task/workplan explicitly changes it",
            "does not adopt it",
            "It never self-adopts a successor",
            "is an adoption candidate, never the source of work bound to the older version",
            "-> only then execute under the successor",
            "Compatibility makes a successor eligible for adoption; it never adopts it",
            "never execute under the loaded successor without explicit adoption",
        ):
            self.assertIn(phrase, self.versioning)
        self.assertNotIn("explicitly adopt a compatible successor", self.versioning)
        self.assertNotIn("use a compatible installed/local source", self.versioning)

    def test_entry_step_forbids_self_adoption_without_new_machinery(self) -> None:
        import build_skills

        step = build_skills.VERSION_STEP_RE.search(self.versioning).group(1)
        for phrase in ("not its source even if newer or compatible", "do not apply it", "report protocol non-closure",
                       "never adopt it yourself", "until the task/workplan authority rebinds it"):
            self.assertIn(phrase, step)
        for path in [*REFS.glob("*.md"), *SOURCE.glob("*.py"), *SOURCE.glob("*/*/SKILL.md")]:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotIn("allow_successor", text)

    def test_preflight_never_resolves_a_cross_minor_successor_as_the_source(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        (tmp / "PROTOCOL_VERSION").write_text("6.6.0\n", encoding="utf-8")
        for governing in ("6.2.0", "6.2", "6.5.0", "6.7.0", "7.0.0"):
            with self.subTest(governing=governing):
                self.assertNotEqual(version_preflight.preflight(tmp, governing, None)["decision"], "CONTINUE")
        self.assertEqual(version_preflight.preflight(tmp, "6.6", None)["decision"], "CONTINUE")


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
