#!/usr/bin/env python3
"""Temporary Protocol 6.1 migration of inherited current-release test assertions."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

contracts_path = ROOT / "tests/test_protocol_contracts.py"
c = contracts_path.read_text(encoding="utf-8")
replacements = (
    ("def test_protocol_60_identity_and_four_domain_roles", "def test_protocol_61_identity_and_four_domain_roles"),
    ('self.assertEqual("6.0.0", read("source/PROTOCOL_VERSION").strip())', 'self.assertEqual("6.1.0", read("source/PROTOCOL_VERSION").strip())'),
    ('self.assertIn("current protocol version: **6.0**", read("README.md").lower())', 'self.assertIn("current protocol version: **6.1**", read("README.md").lower())'),
    ("def test_recursive_abstraction_realization_and_feasibility_are_canonical", "def test_recursive_abstraction_concretization_and_feasibility_are_canonical"),
    ('self.assertIn("abstraction  --design / constrain-->  realization", self.foundation)', 'self.assertIn("abstraction  --design / constrain-->  concretization", self.foundation)'),
    ('self.assertIn("minimum justified realization complexity", self.foundation)', 'self.assertIn("minimum justified concretization complexity", self.foundation)'),
    ('self.assertIn("code/executable behavior is the realization", self.d4)', 'self.assertIn("code/executable behavior is the concretization", self.d4)'),
    ('self.assertIn("realization fidelity", self.foundation)', 'self.assertIn("concretization fidelity", self.foundation)'),
)
for old, new in replacements:
    if old not in c:
        raise RuntimeError(f"missing expected protocol-contract assertion: {old}")
    c = c.replace(old, new)
# Extend, rather than weaken, the current-contract test with the 6.1 evidence owner.
if 'self.evolution = read("source/shared/references/evidence-evolution-and-dependencies.md").lower()' not in c:
    c = c.replace(
        'self.versioning = read("source/shared/references/protocol-versioning-and-compatibility.md").lower()\n',
        'self.versioning = read("source/shared/references/protocol-versioning-and-compatibility.md").lower()\n        self.evolution = read("source/shared/references/evidence-evolution-and-dependencies.md").lower()\n',
    )
    anchor = '    def test_authority_provenance_is_orthogonal_to_domain_level(self) -> None:\n'
    addition = '''    def test_protocol61_evidence_evolution_contract_is_first_class(self) -> None:\n        for phrase in ("evidence specification", "evidence realization", "observation", "evidence assessment", "execution_depends_on"):\n            self.assertIn(phrase, self.evolution)\n        self.assertIn("absence of an edge", self.evolution)\n        self.assertIn("stale", self.evolution)\n\n'''
    if anchor not in c:
        raise RuntimeError("missing insertion anchor in protocol contracts")
    c = c.replace(anchor, addition + anchor)
contracts_path.write_text(c, encoding="utf-8")

quality_path = ROOT / "tests/test_protocol_516_long_horizon_quality.py"
q = quality_path.read_text(encoding="utf-8")
old = 'self.assertEqual("6.0.0", read("source/PROTOCOL_VERSION").strip())'
if old not in q:
    raise RuntimeError("missing current Protocol identity assertion in long-horizon tests")
q = q.replace(old, 'self.assertEqual("6.1.0", read("source/PROTOCOL_VERSION").strip())')
q = q.replace("def test_protocol6_identity_preserves_516_quality_lineage", "def test_protocol61_identity_preserves_516_quality_lineage")
quality_path.write_text(q, encoding="utf-8")

print("Updated inherited current-release tests for Protocol 6.1 without removing behavioral assertions")
