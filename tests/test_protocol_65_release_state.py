from __future__ import annotations

import copy
import re
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
        semantic_ref = candidate["semantic_ref"]
        self.assertTrue(
            semantic_ref == "UNFROZEN" or re.fullmatch(r"[0-9a-f]{40}", semantic_ref),
            semantic_ref,
        )
        self.assertEqual(candidate["review"]["state"], "NOT_RUN")
        self.assertEqual(candidate["ratification"]["state"], "NOT_REQUESTED")
        self.assertEqual(candidate["public_source_ref"], "UNAVAILABLE")
        self.assertEqual(candidate["recovery_ref"], "UNAVAILABLE")

    def test_review_pass_requires_frozen_semantic_candidate(self) -> None:
        data = copy.deepcopy(self.data)
        data["candidate"]["semantic_ref"] = "UNFROZEN"
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
        self.assertTrue(any("RATIFIED" in error and "requires Review PASS" in error for error in errors))

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

    def test_no_pass_review_also_requires_frozen_semantic_candidate(self) -> None:
        data = copy.deepcopy(self.data)
        data["candidate"]["semantic_ref"] = "UNFROZEN"
        data["candidate"]["review"] = {
            "state": "NO_PASS",
            "evidence_ref": "hjin98/scientific-software-development-protocol@" + "a" * 40 + ":qualification/review.md",
        }
        errors = release_state.validate_release_state(data)
        self.assertTrue(any("Review NO_PASS requires" in error for error in errors))

    def test_ratification_cannot_be_pending_or_rejected_before_review_pass(self) -> None:
        for state in ("PENDING", "REJECTED"):
            with self.subTest(state=state):
                data = copy.deepcopy(self.data)
                data["candidate"]["semantic_ref"] = "a" * 40
                data["candidate"]["ratification"] = {
                    "state": state,
                    "evidence_ref": (
                        "NONE" if state == "PENDING"
                        else "hjin98/scientific-software-development-protocol@" + "b" * 40 + ":qualification/ratification.md"
                    ),
                }
                errors = release_state.validate_release_state(data)
                self.assertTrue(any("requires Review PASS" in error for error in errors))

    def test_public_fallback_and_recovery_are_always_distinct(self) -> None:
        data = copy.deepcopy(self.data)
        data["accepted_current"]["recovery_ref"] = data["accepted_current"]["public_source_ref"]
        errors = release_state.validate_release_state(data)
        self.assertTrue(any("accepted_current public_source_ref and recovery_ref must be distinct" in error for error in errors))

        data = copy.deepcopy(self.data)
        data["candidate"]["semantic_ref"] = "a" * 40
        data["candidate"]["review"] = {
            "state": "PASS",
            "evidence_ref": "hjin98/scientific-software-development-protocol@" + "b" * 40 + ":qualification/review.md",
        }
        data["candidate"]["ratification"] = {
            "state": "RATIFIED",
            "evidence_ref": "hjin98/scientific-software-development-protocol@" + "c" * 40 + ":qualification/ratification.md",
        }
        data["candidate"]["public_source_ref"] = "a" * 40
        data["candidate"]["recovery_ref"] = "a" * 40
        errors = release_state.validate_release_state(data)
        self.assertTrue(any("candidate.public_source_ref and candidate.recovery_ref must be distinct" in error for error in errors))

    def test_accepted_current_cannot_cut_over_to_unratified_candidate(self) -> None:
        data = copy.deepcopy(self.data)
        data["accepted_current"] = {
            "version": "6.5.0",
            "public_source_ref": "a" * 40,
            "recovery_ref": "b" * 40,
        }
        errors = release_state.validate_release_state(data)
        self.assertTrue(any("accepted_current cannot equal candidate.version" in error for error in errors))

    def test_historical_state_cannot_duplicate_accepted_current_version(self) -> None:
        data = copy.deepcopy(self.data)
        data["historical"]["6.4.0"] = {
            "public_source_ref": data["accepted_current"]["public_source_ref"],
            "recovery_ref": data["accepted_current"]["recovery_ref"],
        }
        errors = release_state.validate_release_state(data)
        self.assertTrue(any("duplicates accepted_current.version" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
