from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Protocol65PemSchemaParityTests(unittest.TestCase):
    def test_schema_owner_template_and_validator_share_structured_field_contract(self) -> None:
        # Protocol 6.6: schema-1 field semantics live in the cold schema/governance owner.
        owner = (ROOT / "source/shared/references/project-engineering-memory-schema.md").read_text(encoding="utf-8")
        template = (ROOT / "source/shared/templates/project_engineering_memory_template.md").read_text(encoding="utf-8")
        validator = (ROOT / "source/project_engineering_memory.py").read_text(encoding="utf-8")
        for field in (
            "recurrence_basis",
            "maturity_basis",
            "comparative_basis",
            "comparative_authority",
            "temperature_override",
            "counterevidence_search",
            "binding_health",
            "supersedes",
        ):
            with self.subTest(field=field):
                self.assertIn(field, owner)
                self.assertIn(field, template)
                self.assertIn(field, validator)

    def test_redundant_top_level_independence_flag_is_not_current_schema_authority(self) -> None:
        for rel in (
            "source/shared/references/project-engineering-memory.md",
            "source/shared/references/project-engineering-memory-schema.md",
            "source/shared/templates/project_engineering_memory_template.md",
            "source/project_engineering_memory.py",
        ):
            self.assertNotIn(
                "provenance_independence_required",
                (ROOT / rel).read_text(encoding="utf-8"),
                rel,
            )


if __name__ == "__main__":
    unittest.main()
