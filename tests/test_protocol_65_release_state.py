from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
sys.path.insert(0, str(SOURCE))

import release_state  # noqa: E402


class Protocol65ReleaseStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.path = ROOT / "PROTOCOL-RELEASE-STATE.yaml"
        cls.data = yaml.safe_load(cls.path.read_text(encoding="utf-8"))

    def test_repository_release_state_is_coherent_and_refs_realize(self) -> None:
        self.assertEqual(release_state.validate_release_state(self.data, repo_root=ROOT), [])

    def test_current_state_has_one_owner_and_candidate_is_not_prematurely_accepted(self) -> None:
        self.assertEqual(self.data["accepted_current"]["version"], "6.4.0")
        candidate = self.data["candidate"]
        self.assertEqual(candidate["version"], "6.5.0")
        self.assertEqual(candidate["semantic_ref"], "UNFROZEN")
        self.assertEqual(candidate["review"]["state"], "NOT_RUN")
        self.assertEqual(candidate["ratification"]["state"], "NOT_REQUESTED")
        self.assertEqual(candidate["public_source_ref"], "UNAVAILABLE")
        self.assertEqual(candidate["recovery_ref"], "UNAVAILABLE")

    def test_review_pass_requires_frozen_semantic_candidate(self) -> None:
        data = copy.deepcopy(self.data)
        data["candidate"]["review"] = {
            "state": "PASS",
            "evidence_ref": "hjin98/scientific-software-development-protocol@" + "a" * 40 + ":qualification/review.md",
        }
        errors = release_state.validate_release_state(data)
        self.assertTrue(any("Review PASS requires" in error for error in errors))

    def test_ratification_cannot_self_promote_without_review(self) -> None:
        data = copy.deepcopy(self.data)
        data["candidate"]["semantic_ref"] = "a" * 40
        data["candidate"]["ratification"] = {
            "state": "RATIFIED",
            "evidence_ref": "hjin98/scientific-software-development-protocol@" + "b" * 40 + ":qualification/ratification.md",
        }
        errors = release_state.validate_release_state(data)
        self.assertTrue(any("RATIFIED requires Review PASS" in error for error in errors))

    def test_public_fallback_requires_review_ratification_and_exact_candidate(self) -> None:
        data = copy.deepcopy(self.data)
        data["candidate"]["semantic_ref"] = "a" * 40
        data["candidate"]["public_source_ref"] = "b" * 40
        errors = release_state.validate_release_state(data)
        self.assertTrue(any("requires Review PASS and RATIFIED" in error for error in errors))
        self.assertTrue(any("must equal the exact reviewed/ratified" in error for error in errors))

    def test_recovery_cannot_precede_public_fallback(self) -> None:
        data = copy.deepcopy(self.data)
        data["candidate"]["recovery_ref"] = "a" * 40
        errors = release_state.validate_release_state(data)
        self.assertTrue(any("recovery_ref requires" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
