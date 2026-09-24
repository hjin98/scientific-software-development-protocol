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

    def _review_evidence_errors(
        self,
        *,
        evidence_ref: str,
        semantic_ref: str,
        review_state: str,
        git_results: list[tuple[int, str]],
    ) -> list[str]:
        errors: list[str] = []
        with mock.patch.object(release_state, "_git", side_effect=git_results):
            release_state._check_review_evidence(
                ROOT,
                "hjin98/scientific-software-development-protocol",
                evidence_ref,
                semantic_ref,
                review_state,
                "candidate.review.evidence_ref",
                errors,
            )
        return errors

    def test_review_evidence_binds_exact_candidate_and_disposition(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/review.md"
        )
        review = f"""---
status: pass
p1: {candidate}
---
# Review
"""
        self.assertEqual(
            self._review_evidence_errors(
                evidence_ref=evidence_ref,
                semantic_ref=candidate,
                review_state="PASS",
                git_results=[(0, ""), (0, review)],
            ),
            [],
        )

    def test_review_evidence_rejects_wrong_candidate(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/review.md"
        )
        review = f"""---
status: pass
p1: {"c" * 40}
---
# Review
"""
        errors = self._review_evidence_errors(
            evidence_ref=evidence_ref,
            semantic_ref=candidate,
            review_state="PASS",
            git_results=[(0, ""), (0, review)],
        )
        self.assertTrue(any("does not bind candidate.semantic_ref" in error for error in errors))

    def test_review_evidence_rejects_disposition_mismatch(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/review.md"
        )
        review = f"""---
status: no-pass
p1: {candidate}
---
# Review
"""
        errors = self._review_evidence_errors(
            evidence_ref=evidence_ref,
            semantic_ref=candidate,
            review_state="PASS",
            git_results=[(0, ""), (0, review)],
        )
        self.assertTrue(any("does not match candidate.review.state PASS" in error for error in errors))

    def test_review_evidence_rejects_wrong_repository(self) -> None:
        errors: list[str] = []
        release_state._check_review_evidence(
            ROOT,
            "hjin98/scientific-software-development-protocol",
            "other/project@" + "b" * 40 + ":qualification/review.md",
            "a" * 40,
            "PASS",
            "candidate.review.evidence_ref",
            errors,
        )
        self.assertTrue(any("must identify evidence in project" in error for error in errors))

    def test_review_evidence_rejects_missing_commit_or_path(self) -> None:
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/review.md"
        )
        errors = self._review_evidence_errors(
            evidence_ref=evidence_ref,
            semantic_ref="a" * 40,
            review_state="PASS",
            git_results=[(1, "")],
        )
        self.assertTrue(any("commit" in error and "not resolvable" in error for error in errors))

        errors = self._review_evidence_errors(
            evidence_ref=evidence_ref,
            semantic_ref="a" * 40,
            review_state="PASS",
            git_results=[(0, ""), (1, "")],
        )
        self.assertTrue(any("is not readable at commit" in error for error in errors))

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
