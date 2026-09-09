#!/usr/bin/env python3
"""Temporary Protocol 6.1 lossless-migration reconciliation.

This helper runs after ssdp61_finalize.py. It repairs over-compressed current
surfaces by restoring inherited Protocol 6.0 semantics, then migrates only the
intentional 6.1 terminology/version oracles. No acceptance assertion is removed.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing migration anchor {label}: {old[:100]!r}")
    return text.replace(old, new)


def migrate_semantic_realization(text: str) -> str:
    """Move semantic-descent realization vocabulary to concretization.

    Evidence-realization phrases and opaque compatibility filenames remain
    protected because Protocol 6.1 reserves realization for evidence execution.
    """
    protected = {
        "abstraction-and-realization.md": "__SSDP_ABSTRACTION_REALIZATION_FILE__",
        "abstraction_realization_change_plan_template.md": "__SSDP_ABSTRACTION_REALIZATION_TEMPLATE__",
        "evidence realizations": "__SSDP_EVIDENCE_REALIZATIONS__",
        "evidence realization": "__SSDP_EVIDENCE_REALIZATION__",
        "Evidence realizations": "__SSDP_EVIDENCE_REALIZATIONS_CAP__",
        "Evidence realization": "__SSDP_EVIDENCE_REALIZATION_CAP__",
    }
    for old, sentinel in protected.items():
        text = text.replace(old, sentinel)
    replacements = (
        (r"\bunrealizable\b", "impossible to concretize"),
        (r"\bUnrealizable\b", "Impossible to concretize"),
        (r"\brealizations\b", "concretizations"),
        (r"\bRealizations\b", "Concretizations"),
        (r"\brealization\b", "concretization"),
        (r"\bRealization\b", "Concretization"),
        (r"\brealizes\b", "concretizes"),
        (r"\bRealizes\b", "Concretizes"),
        (r"\brealized\b", "concretized"),
        (r"\bRealized\b", "Concretized"),
        (r"\brealizing\b", "concretizing"),
        (r"\bRealizing\b", "Concretizing"),
        (r"\brealize\b", "concretize"),
        (r"\bRealize\b", "Concretize"),
    )
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)
    for old, sentinel in protected.items():
        text = text.replace(sentinel, old)
    return text


# ---------------------------------------------------------------------------
# Restore the complete accepted Protocol 6.0 orchestration semantics, then
# apply only the 6.1 vocabulary/repository/evidence additions. This replaces
# the earlier over-compressed prompt rewrite and preserves all 5.16/6.0 gates.
# ---------------------------------------------------------------------------
frozen_prompt = ROOT / "orchestrator/src/sdp_orchestrator/core/resources/protocol/ssdp-protocol-6.0/prompts.md"
prompt_path = ROOT / "source/shared/references/development-workflow-prompts.md"
prompt = frozen_prompt.read_text(encoding="utf-8")
prompt = prompt.replace("https://github.com/hjin98/software-development-protocol", "https://github.com/hjin98/scientific-software-development-protocol")
prompt = prompt.replace("Protocol 6", "Protocol 6.1")
prompt = migrate_semantic_realization(prompt)

# Add the 6.1 evidence/evolution layer once, without changing the 11-stage
# machine-parsed heading/input contract inherited from 6.0.
evidence_section = '''## Evidence applicability and impact closure\n\nProtocol 6.1 distinguishes an **evidence specification** from an **evidence realization**, its **observation**, and the resulting **evidence assessment**. A stale passing observation cannot confirm current authority and a stale failing observation cannot refute it until applicability is restored. Keep the governed evidentiary target distinct from replaceable execution dependencies.\n\nWhen accepted authority or a material concretization changes, perform bounded manual impact closure over materially dependent descendants, evidence specifications/realizations, documentation/current dependency views, re-ratification obligations, retirement/cleanup, and semantic-evolution history. Preserve unaffected siblings and still-admissible evidence. Absence of an edge in a partial dependency view is not proof of independence.\n\n'''
marker = "## Stage-selection rule of thumb\n"
if marker not in prompt:
    raise RuntimeError("stage-selection heading missing from frozen prompt")
prompt = prompt.replace(marker, evidence_section + marker, 1)

# Carry the new evidence obligations into the most relevant execution stages.
prompt = prompt.replace(
    "Close every material executable stage semantically plus focused/stage-local affected regression. Before completion reconcile the full accepted contract, inspect obsolete/bypassed/duplicate ownership and complexity, re-derive the final affected surface, run complete affected regression, real-owner integration/end-to-end, and repository/project-required checks. A required check not executed is not a pass.\n",
    "Close every material executable stage semantically plus focused/stage-local affected regression. Before completion reconcile the full accepted contract, inspect obsolete/bypassed/duplicate ownership and complexity, re-derive the final affected surface, run complete affected regression, real-owner integration/end-to-end, and repository/project-required checks. Reconcile materially affected evidence applicability, dependency views, and semantic-history obligations before closure. A required check or material impact item not closed is not a pass.\n",
)
prompt = prompt.replace(
    "Missing required regression/integration/repository checks remain blockers.",
    "Missing required regression/integration/repository checks and unresolved material evidence/dependency impact items remain blockers. Stale or otherwise inadmissible evidence cannot satisfy a current acceptance claim.",
)
prompt = prompt.replace(
    "Reconcile only materially dependent assumptions/invariants/evidence after UPSTREAM_ACCEPTED_WORK. Preserve unaffected siblings and still-valid evidence.",
    "Reconcile only materially dependent assumptions/invariants/evidence after UPSTREAM_ACCEPTED_WORK. Preserve unaffected siblings and still-valid evidence. A missing edge in a partial dependency view is not proof of non-impact.",
)
prompt = prompt.replace(
    "Reconcile accepted-current D1-D4 authority, guides/runbooks, generated artifacts, release/version information, and completed/superseded workplan state.",
    "Reconcile accepted-current D1-D4 authority, guides/runbooks, generated artifacts, release/version information, current dependency/evidence views, semantic-evolution history where triggered, and completed/superseded workplan state.",
)
prompt_path.write_text(prompt, encoding="utf-8")

# ---------------------------------------------------------------------------
# Restore two discoverability/ownership sentences that were semantically lost
# from the current workflow refactor.
# ---------------------------------------------------------------------------
workflow_path = ROOT / "source/shared/references/workflow-and-workplans.md"
w = workflow_path.read_text(encoding="utf-8")
role_sentence = "Supporting capabilities such as `software-documentation`, `software-maintenance-audit`, and `repository-hygiene` are not authority-bearing approval roles."
if role_sentence in w and "not a third lifecycle role" not in w:
    w = w.replace(role_sentence, role_sentence + " In particular, `software-maintenance-audit` is not a third lifecycle role; it is non-authoritative longitudinal sensing/support.")
active_anchor = "## Active simplicity and recurrence\n"
if "convergence-and-cycle-economy.md" not in w:
    w = replace_required(
        w,
        active_anchor,
        active_anchor + "\nDetailed recurrence, bounded family closure, simplification, review-sufficiency, and revision-economy rules route through [Convergence and development-cycle economy](convergence-and-cycle-economy.md).\n",
        "workflow convergence route",
    )
workflow_path.write_text(w, encoding="utf-8")

# ---------------------------------------------------------------------------
# Current role/specialist prose must use concretization for semantic descent.
# Preserve the legacy reference/template filenames and evidence-realization term.
# ---------------------------------------------------------------------------
for rel in (
    "source/roles/software-design/SKILL.md",
    "source/roles/software-implementation/SKILL.md",
    "source/specialists/software-documentation/SKILL.md",
    "source/specialists/software-maintenance-audit/SKILL.md",
    "source/specialists/repository-hygiene/SKILL.md",
):
    path = ROOT / rel
    path.write_text(migrate_semantic_realization(path.read_text(encoding="utf-8")), encoding="utf-8")

# ---------------------------------------------------------------------------
# Remove duplicated package-resource authority: package exactly the Markdown
# routes each SKILL.md exposes. The explicit role/specialist registries remain
# authoritative for skill identity; direct links own payload composition.
# ---------------------------------------------------------------------------
build_path = ROOT / "source/build_skills.py"
b = build_path.read_text(encoding="utf-8")
insert_anchor = "NAME_RE = re.compile(r\"(?m)^name:\\\\s*([a-z0-9]+(?:-[a-z0-9]+)*)\\\\s*$\")"
# The literal source uses a raw regex; locate by the simpler declaration prefix.
pos = b.find("NAME_RE = re.compile")
if pos < 0:
    raise RuntimeError("build_skills NAME_RE anchor missing")
route_code = r'''DIRECT_ROUTE_RE = re.compile(r"\]\((?P<kind>references|templates)/(?P<name>[A-Za-z0-9_.-]+\.md)\)")


def _direct_payload(root: Path, skill_name: str) -> tuple[list[str], list[str]]:
    text = (root / skill_name / "SKILL.md").read_text(encoding="utf-8")
    references: list[str] = []
    templates: list[str] = []
    for match in DIRECT_ROUTE_RE.finditer(text):
        target = references if match.group("kind") == "references" else templates
        name = match.group("name")
        if name not in target:
            target.append(name)
    return references, templates


for _name, _spec in ROLE_SPECS.items():
    _spec["references"], _spec["templates"] = _direct_payload(ROLES, _name)
for _name, _spec in SPECIALIST_SPECS.items():
    _spec["references"], _spec["templates"] = _direct_payload(SPECIALISTS, _name)


'''
if "DIRECT_ROUTE_RE" not in b:
    b = b[:pos] + route_code + b[pos:]
build_path.write_text(b, encoding="utf-8")

# ---------------------------------------------------------------------------
# Migrate inherited regression oracles only where Protocol 6.1 intentionally
# changed vocabulary/version/repository identity or abbreviation presentation.
# Behavioral assertions themselves remain intact.
# ---------------------------------------------------------------------------

def patch_file(rel: str, replacements: tuple[tuple[str, str], ...]) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        if old not in text:
            raise RuntimeError(f"{rel}: missing expected oracle {old!r}")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


patch_file("tests/test_protocol_contracts.py", (
    ("def test_protocol_60_identity_and_four_domain_roles", "def test_protocol_61_identity_and_four_domain_roles"),
    ('self.assertEqual("6.0.0", read("source/PROTOCOL_VERSION").strip())', 'self.assertEqual("6.1.0", read("source/PROTOCOL_VERSION").strip())'),
    ('self.assertIn("current protocol version: **6.0**", read("README.md").lower())', 'self.assertIn("current protocol version: **6.1**", read("README.md").lower())'),
    ("def test_recursive_abstraction_realization_and_feasibility_are_canonical", "def test_recursive_abstraction_concretization_and_feasibility_are_canonical"),
    ('self.assertIn("abstraction  --design / constrain-->  realization", self.foundation)', 'self.assertIn("abstraction  --design / constrain-->  concretization", self.foundation)'),
    ('self.assertIn("minimum justified realization complexity", self.foundation)', 'self.assertIn("minimum justified concretization complexity", self.foundation)'),
    ('self.assertIn("code/executable behavior is the realization", self.d4)', 'self.assertIn("code/executable behavior is the concretization", self.d4)'),
    ('self.assertIn("realization fidelity", self.foundation)', 'self.assertIn("concretization fidelity", self.foundation)'),
    ('self.assertIn("do not reinterpret active or completed 5.x work using protocol 6", self.versioning)', 'self.assertIn("do not reinterpret active or completed 5.x or 6.0 work using protocol 6.1", self.versioning)'),
))
contracts = ROOT / "tests/test_protocol_contracts.py"
c = contracts.read_text(encoding="utf-8")
if 'self.evolution = read("source/shared/references/evidence-evolution-and-dependencies.md").lower()' not in c:
    c = c.replace(
        'self.versioning = read("source/shared/references/protocol-versioning-and-compatibility.md").lower()\n',
        'self.versioning = read("source/shared/references/protocol-versioning-and-compatibility.md").lower()\n        self.evolution = read("source/shared/references/evidence-evolution-and-dependencies.md").lower()\n',
    )
    anchor = '    def test_authority_provenance_is_orthogonal_to_domain_level(self) -> None:\n'
    addition = '''    def test_protocol61_evidence_evolution_contract_is_first_class(self) -> None:\n        for phrase in ("evidence specification", "evidence realization", "observation", "evidence assessment", "execution_depends_on"):\n            self.assertIn(phrase, self.evolution)\n        self.assertIn("absence of an edge", self.evolution)\n        self.assertIn("stale", self.evolution)\n\n'''
    c = replace_required(c, anchor, addition + anchor, "contract evidence test insertion")
contracts.write_text(c, encoding="utf-8")

patch_file("tests/test_protocol_512_convergence.py", (
    ("does not answer whether the current realization should survive", "does not answer whether the current concretization should survive"),
    ("re-derive and simplify the delegated realization", "re-derive and simplify the delegated concretization"),
    ("active simplification/re-derivation of delegated realization is required", "active simplification/re-derivation of delegated concretization is required"),
    ("delegated realization", "delegated concretization"),
))

patch_file("tests/test_protocol_515_language_profiles.py", (
    (r"implementation-local realization", r"implementation-local concretization"),
    ("current protocol 6 domain doctrine is authoritative", "current protocol 6.1 domain doctrine is authoritative"),
    ("gil-constrained", "global-interpreter-lock (gil)-constrained"),
    ("## architecture-gated accelerator realization", "## architecture-gated accelerator concretization"),
    ("## accelerator realization", "## accelerator concretization"),
    ("active older workplans do not automatically adopt protocol 5.16 or any later release", "active older workplans may continue under their declared version"),
))

patch_file("tests/test_protocol_516_long_horizon_quality.py", (
    ('self.assertEqual("6.0.0", read("source/PROTOCOL_VERSION").strip())', 'self.assertEqual("6.1.0", read("source/PROTOCOL_VERSION").strip())'),
    ("def test_protocol6_identity_preserves_516_quality_lineage", "def test_protocol61_identity_preserves_516_quality_lineage"),
))

patch_file("tests/test_protocol_516_orchestration.py", (
    ("https://github.com/hjin98/software-development-protocol", "https://github.com/hjin98/scientific-software-development-protocol"),
    ("blocks protocol 6 release", "blocks protocol 6.1 release"),
))

patch_file("tests/test_protocol_effective_compression.py", (
    ("expensive ml/scientific training or prediction", "expensive machine-learning/scientific training or prediction"),
    ("test_equivalent_local_realization_is_reconciliation_not_redesign", "test_equivalent_local_concretization_is_reconciliation_not_redesign"),
    ("equivalent local realization", "equivalent local concretization"),
    ("suggested realization does not become a cycle-scoped or durable authority", "suggested concretization does not become a cycle-scoped or durable authority"),
    ("literal compliance actually realizes the protected stakeholder outcome", "literal compliance actually concretizes the protected stakeholder outcome"),
    ("delegated realization beneath the governing abstraction", "delegated concretization beneath the governing abstraction"),
))

patch_file("tests/test_protocol_engineering_stewardship.py", (
    ("literal compliance actually realizes the protected stakeholder outcome", "literal compliance actually concretizes the protected stakeholder outcome"),
    ("anti-shortcut / integrity constraint", "anti-shortcut/integrity constraint"),
))

patch_file("tests/test_protocol_portability.py", (
    ("test_current_protocol_uses_abstraction_realization_hierarchy", "test_current_protocol_uses_abstraction_concretization_hierarchy"),
    ("minimum justified realization complexity", "minimum justified concretization complexity"),
))

patch_file("tests/test_protocol_proxy_proof_acceptance.py", (
    ("expensive ml/scientific training or prediction", "expensive machine-learning/scientific training or prediction"),
    ("real semantic owner/path of the final accepted realization", "real semantic owner/path of the final accepted concretization"),
    ("merely the current delegated realization", "merely the current delegated concretization"),
    ("final accepted realization", "final accepted concretization"),
    ("do not require universal ast scanning", "do not require universal abstract-syntax-tree (ast) scanning"),
))

# New 6.1 tests should follow the settled ABG example and central authority's
# actual reservation sentence instead of manufacturing a second example token.
patch_file("tests/test_protocol_61_evidence_evolution.py", (
    ('self.assertIn("evidence realization", authority)', 'self.assertIn("**realization** is reserved for concrete evidence execution", authority)'),
    ('self.assertIn("full term (ABC)", writing)', 'self.assertIn("alpha beta gamma (ABG)", writing)'),
))

# The current Protocol 6.1 prompt is deliberately derived from the frozen 6.0
# prompt source plus 6.1 semantics. Its current-public URL is the canonical repo.
# The inherited orchestration test otherwise remains unchanged.

print("Reconciled inherited Protocol capabilities and migrated only intentional 6.1 oracles")
