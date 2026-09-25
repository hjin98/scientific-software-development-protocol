from __future__ import annotations

import copy
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
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
        cls.data = release_state.load(cls.path)

    def test_repository_release_state_is_coherent_and_refs_realize(self) -> None:
        self.assertEqual(release_state.validate_release_state(self.data, repo_root=ROOT), [])


    def test_release_state_load_rejects_duplicate_mapping_keys(self) -> None:
        records = (
            """schema_version: 1
schema_version: 1
""",
            """candidate:
  version: "6.5.0"
  semantic_ref: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  semantic_ref: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
""",
            """candidate:
  review:
    state: NOT_RUN
    state: PASS
""",
            """accepted_current:
  version: "6.4.0"
  public_source_ref: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  public_source_ref: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
""",
            """historical:
  "6.3.0":
    public_source_ref: NONE
  "6.3.0":
    public_source_ref: NONE
""",
        )
        for record in records:
            with self.subTest(record=record):
                with tempfile.TemporaryDirectory() as tmpdir:
                    path = Path(tmpdir) / "state.yaml"
                    path.write_text(record, encoding="utf-8")
                    with self.assertRaisesRegex(
                        yaml.constructor.ConstructorError,
                        "found duplicate key",
                    ):
                        release_state.load(path)

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

    def _ratification_evidence_errors(
        self,
        *,
        evidence_ref: str,
        semantic_ref: str,
        ratification_state: str,
        git_results: list[tuple[int, str]],
    ) -> list[str]:
        errors: list[str] = []
        with mock.patch.object(release_state, "_git", side_effect=git_results):
            release_state._check_ratification_evidence(
                ROOT,
                "hjin98/scientific-software-development-protocol",
                evidence_ref,
                semantic_ref,
                ratification_state,
                "candidate.ratification.evidence_ref",
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

    def test_review_evidence_accepts_generic_future_candidate_key(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/review.md"
        )
        review = f"""---
status: pass
p5: {candidate}
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

    def test_review_evidence_rejects_explicit_subject_hidden_by_historical_pn(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/review.md"
        )
        for field in ("candidate_ref", "semantic_ref"):
            with self.subTest(field=field):
                review = f"""---
status: pass
{field}: {"c" * 40}
p3: {candidate}
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

    def test_review_evidence_uses_highest_legacy_candidate_generation(self) -> None:
        p3 = "a" * 40
        p4 = "c" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/review.md"
        )
        review = f"""---
status: pass
p3: {p3}
p4: {p4}
---
# Review
"""
        errors = self._review_evidence_errors(
            evidence_ref=evidence_ref,
            semantic_ref=p3,
            review_state="PASS",
            git_results=[(0, ""), (0, review)],
        )
        self.assertTrue(any("does not bind candidate.semantic_ref" in error for error in errors))
        self.assertEqual(
            self._review_evidence_errors(
                evidence_ref=evidence_ref,
                semantic_ref=p4,
                review_state="PASS",
                git_results=[(0, ""), (0, review)],
            ),
            [],
        )

    def test_review_evidence_rejects_conflicting_explicit_subject_fields(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/review.md"
        )
        review = f"""---
status: pass
candidate_ref: {candidate}
semantic_ref: {"c" * 40}
---
# Review
"""
        errors = self._review_evidence_errors(
            evidence_ref=evidence_ref,
            semantic_ref=candidate,
            review_state="PASS",
            git_results=[(0, ""), (0, review)],
        )
        self.assertTrue(any("conflicting explicit candidate subject fields" in error for error in errors))

    def test_review_evidence_rejects_duplicate_front_matter_keys(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/review.md"
        )
        records = (
            f"""---
status: pass
candidate_ref: {"c" * 40}
candidate_ref: {candidate}
---
# Review
""",
            f"""---
status: pass
semantic_ref: {"c" * 40}
semantic_ref: {candidate}
---
# Review
""",
            f"""---
status: no-pass
status: pass
candidate_ref: {candidate}
---
# Review
""",
        )
        for review in records:
            with self.subTest(review=review):
                errors = self._review_evidence_errors(
                    evidence_ref=evidence_ref,
                    semantic_ref=candidate,
                    review_state="PASS",
                    git_results=[(0, ""), (0, review)],
                )
                self.assertTrue(any("duplicate key" in error for error in errors))

    def test_review_evidence_rejects_present_invalid_explicit_subject_before_legacy_fallback(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/review.md"
        )
        for field, value in (("candidate_ref", ""), ("semantic_ref", "null"), ("candidate_ref", "not-a-sha")):
            with self.subTest(field=field, value=value):
                review = f"""---
status: pass
{field}: {value}
p4: {candidate}
---
# Review
"""
                errors = self._review_evidence_errors(
                    evidence_ref=evidence_ref,
                    semantic_ref=candidate,
                    review_state="PASS",
                    git_results=[(0, ""), (0, review)],
                )
                self.assertTrue(any("explicit" in error and "40-hex" in error for error in errors))

    def test_review_evidence_rejects_empty_higher_legacy_generation(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/review.md"
        )
        review = f"""---
status: pass
p4: {candidate}
p5:
---
# Review
"""
        errors = self._review_evidence_errors(
            evidence_ref=evidence_ref,
            semantic_ref=candidate,
            review_state="PASS",
            git_results=[(0, ""), (0, review)],
        )
        self.assertTrue(any("legacy candidate subject field p5" in error for error in errors))

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

    def test_evidence_routes_reject_unsafe_paths(self) -> None:
        for path in ("../qualification/review.md", "/qualification/review.md"):
            with self.subTest(path=path):
                errors: list[str] = []
                release_state._check_review_evidence(
                    ROOT,
                    "hjin98/scientific-software-development-protocol",
                    "hjin98/scientific-software-development-protocol@"
                    + "b" * 40
                    + ":"
                    + path,
                    "a" * 40,
                    "PASS",
                    "candidate.review.evidence_ref",
                    errors,
                )
                self.assertTrue(any("repository-relative" in error for error in errors))

    def test_ratification_evidence_binds_exact_candidate_and_disposition(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/ratification.md"
        )
        ratification = f"""---
status: ratified
candidate_ref: {candidate}
---
# Stakeholder ratification
"""
        self.assertEqual(
            self._ratification_evidence_errors(
                evidence_ref=evidence_ref,
                semantic_ref=candidate,
                ratification_state="RATIFIED",
                git_results=[(0, ""), (0, ratification)],
            ),
            [],
        )

    def test_ratification_evidence_rejects_wrong_candidate(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/ratification.md"
        )
        ratification = f"""---
status: ratified
candidate_ref: {"c" * 40}
---
# Stakeholder ratification
"""
        errors = self._ratification_evidence_errors(
            evidence_ref=evidence_ref,
            semantic_ref=candidate,
            ratification_state="RATIFIED",
            git_results=[(0, ""), (0, ratification)],
        )
        self.assertTrue(any("does not bind candidate.semantic_ref" in error for error in errors))

    def test_ratification_evidence_rejects_disposition_mismatch(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/ratification.md"
        )
        ratification = f"""---
status: rejected
semantic_ref: {candidate}
---
# Stakeholder ratification
"""
        errors = self._ratification_evidence_errors(
            evidence_ref=evidence_ref,
            semantic_ref=candidate,
            ratification_state="RATIFIED",
            git_results=[(0, ""), (0, ratification)],
        )
        self.assertTrue(any("does not match candidate.ratification.state RATIFIED" in error for error in errors))

    def test_ratification_evidence_rejects_wrong_repository(self) -> None:
        errors: list[str] = []
        release_state._check_ratification_evidence(
            ROOT,
            "hjin98/scientific-software-development-protocol",
            "other/project@" + "b" * 40 + ":qualification/ratification.md",
            "a" * 40,
            "RATIFIED",
            "candidate.ratification.evidence_ref",
            errors,
        )
        self.assertTrue(any("must identify evidence in project" in error for error in errors))

    def test_ratification_evidence_rejects_missing_commit_or_path(self) -> None:
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/ratification.md"
        )
        errors = self._ratification_evidence_errors(
            evidence_ref=evidence_ref,
            semantic_ref="a" * 40,
            ratification_state="RATIFIED",
            git_results=[(1, "")],
        )
        self.assertTrue(any("commit" in error and "not resolvable" in error for error in errors))

        errors = self._ratification_evidence_errors(
            evidence_ref=evidence_ref,
            semantic_ref="a" * 40,
            ratification_state="RATIFIED",
            git_results=[(0, ""), (1, "")],
        )
        self.assertTrue(any("is not readable at commit" in error for error in errors))

    def test_ratification_evidence_rejects_explicit_subject_hidden_by_historical_pn(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/ratification.md"
        )
        ratification = f"""---
status: ratified
candidate_ref: {"c" * 40}
p3: {candidate}
---
# Stakeholder ratification
"""
        errors = self._ratification_evidence_errors(
            evidence_ref=evidence_ref,
            semantic_ref=candidate,
            ratification_state="RATIFIED",
            git_results=[(0, ""), (0, ratification)],
        )
        self.assertTrue(any("does not bind candidate.semantic_ref" in error for error in errors))

    def test_ratification_evidence_uses_highest_legacy_candidate_generation(self) -> None:
        p3 = "a" * 40
        p4 = "c" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/ratification.md"
        )
        ratification = f"""---
status: ratified
p3: {p3}
p4: {p4}
---
# Stakeholder ratification
"""
        errors = self._ratification_evidence_errors(
            evidence_ref=evidence_ref,
            semantic_ref=p3,
            ratification_state="RATIFIED",
            git_results=[(0, ""), (0, ratification)],
        )
        self.assertTrue(any("does not bind candidate.semantic_ref" in error for error in errors))
        self.assertEqual(
            self._ratification_evidence_errors(
                evidence_ref=evidence_ref,
                semantic_ref=p4,
                ratification_state="RATIFIED",
                git_results=[(0, ""), (0, ratification)],
            ),
            [],
        )

    def test_ratification_evidence_accepts_future_legacy_generation(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/ratification.md"
        )
        ratification = f"""---
status: ratified
p5: {candidate}
---
# Stakeholder ratification
"""
        self.assertEqual(
            self._ratification_evidence_errors(
                evidence_ref=evidence_ref,
                semantic_ref=candidate,
                ratification_state="RATIFIED",
                git_results=[(0, ""), (0, ratification)],
            ),
            [],
        )

    def test_ratification_evidence_rejects_duplicate_front_matter_keys(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/ratification.md"
        )
        records = (
            f"""---
status: ratified
candidate_ref: {"c" * 40}
candidate_ref: {candidate}
---
# Stakeholder ratification
""",
            f"""---
status: ratified
semantic_ref: {"c" * 40}
semantic_ref: {candidate}
---
# Stakeholder ratification
""",
            f"""---
status: rejected
status: ratified
candidate_ref: {candidate}
---
# Stakeholder ratification
""",
        )
        for ratification in records:
            with self.subTest(ratification=ratification):
                errors = self._ratification_evidence_errors(
                    evidence_ref=evidence_ref,
                    semantic_ref=candidate,
                    ratification_state="RATIFIED",
                    git_results=[(0, ""), (0, ratification)],
                )
                self.assertTrue(any("duplicate key" in error for error in errors))

    def test_ratification_evidence_rejects_present_invalid_explicit_subject_before_legacy_fallback(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/ratification.md"
        )
        for field, value in (("candidate_ref", ""), ("semantic_ref", "null"), ("semantic_ref", "not-a-sha")):
            with self.subTest(field=field, value=value):
                ratification = f"""---
status: ratified
{field}: {value}
p4: {candidate}
---
# Stakeholder ratification
"""
                errors = self._ratification_evidence_errors(
                    evidence_ref=evidence_ref,
                    semantic_ref=candidate,
                    ratification_state="RATIFIED",
                    git_results=[(0, ""), (0, ratification)],
                )
                self.assertTrue(any("explicit" in error and "40-hex" in error for error in errors))

    def test_ratification_evidence_rejects_conflicting_explicit_subject_fields(self) -> None:
        candidate = "a" * 40
        evidence_ref = (
            "hjin98/scientific-software-development-protocol@"
            + "b" * 40
            + ":qualification/ratification.md"
        )
        ratification = f"""---
status: ratified
candidate_ref: {candidate}
semantic_ref: {"c" * 40}
---
# Stakeholder ratification
"""
        errors = self._ratification_evidence_errors(
            evidence_ref=evidence_ref,
            semantic_ref=candidate,
            ratification_state="RATIFIED",
            git_results=[(0, ""), (0, ratification)],
        )
        self.assertTrue(any("conflicting explicit candidate subject fields" in error for error in errors))

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
        data["candidate"]["review"] = {"state": "NOT_RUN", "evidence_ref": "NONE"}
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
                data["candidate"]["review"] = {"state": "NOT_RUN", "evidence_ref": "NONE"}
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

    def test_active_candidate_rejects_historical_or_older_version(self) -> None:
        data = copy.deepcopy(self.data)
        data["candidate"] = {
            "version": "6.3.0",
            "semantic_ref": "9f353097fab36e325a325f1c2f9d9cec32e86177",
            "review": {"state": "NOT_RUN", "evidence_ref": "NONE"},
            "ratification": {"state": "NOT_REQUESTED", "evidence_ref": "NONE"},
            "public_source_ref": "UNAVAILABLE",
            "recovery_ref": "UNAVAILABLE",
        }
        errors = release_state.validate_release_state(data, repo_root=ROOT)
        self.assertTrue(any("duplicates a historical version" in error for error in errors))
        self.assertTrue(any("must be newer than accepted_current.version" in error for error in errors))

        data = copy.deepcopy(self.data)
        data["candidate"] = {
            "version": "6.3.1",
            "semantic_ref": "UNFROZEN",
            "review": {"state": "NOT_RUN", "evidence_ref": "NONE"},
            "ratification": {"state": "NOT_REQUESTED", "evidence_ref": "NONE"},
            "public_source_ref": "UNAVAILABLE",
            "recovery_ref": "UNAVAILABLE",
        }
        errors = release_state.validate_release_state(data)
        self.assertTrue(any("must be newer than accepted_current.version" in error for error in errors))
        self.assertFalse(any("duplicates a historical version" in error for error in errors))

    def test_historical_versions_must_precede_accepted_current(self) -> None:
        data = copy.deepcopy(self.data)
        data["historical"]["6.5.0"] = {
            "public_source_ref": "dd06da8136416e67644586c44880b466f982b8ff",
            "recovery_ref": "758490c11f90b587c7dfaadddab958751f2881c9",
        }
        data["candidate"] = {
            "version": "6.6.0",
            "semantic_ref": "UNFROZEN",
            "review": {"state": "NOT_RUN", "evidence_ref": "NONE"},
            "ratification": {"state": "NOT_REQUESTED", "evidence_ref": "NONE"},
            "public_source_ref": "UNAVAILABLE",
            "recovery_ref": "UNAVAILABLE",
        }
        errors = release_state.validate_release_state(data, repo_root=ROOT)
        self.assertTrue(
            any(
                "historical[6.5.0] must be older than accepted_current.version 6.4.0" in error
                for error in errors
            )
        )
        self.assertFalse(
            any("historical[6.5.0].public_source_ref maps" in error for error in errors)
        )
        self.assertFalse(
            any("historical[6.5.0].recovery_ref maps" in error for error in errors)
        )

    def test_version_identity_requires_canonical_ascii_semver(self) -> None:
        candidate_forms = ("06.5.0", "6.05.0", "6.5.00", "٦.٥.٠")
        for version in candidate_forms:
            with self.subTest(surface="candidate", version=version):
                data = copy.deepcopy(self.data)
                data["candidate"]["version"] = version
                errors = release_state.validate_release_state(data)
                self.assertTrue(any("candidate.version must be semantic x.y.z" in error for error in errors))

        for version in ("06.3.0", "6.03.0", "٦.٣.٠"):
            with self.subTest(surface="historical", version=version):
                data = copy.deepcopy(self.data)
                data["historical"][version] = data["historical"].pop("6.3.0")
                errors = release_state.validate_release_state(data)
                self.assertTrue(any("historical version key" in error for error in errors))

        for version in ("06.4.0", "6.04.0", "٦.٤.٠"):
            with self.subTest(surface="accepted_current", version=version):
                data = copy.deepcopy(self.data)
                data["accepted_current"]["version"] = version
                errors = release_state.validate_release_state(data)
                self.assertTrue(
                    any("accepted_current.version must be semantic x.y.z" in error for error in errors)
                )

    def test_active_candidate_accepts_patch_minor_and_major_successors(self) -> None:
        for version in ("6.4.1", "6.5.0", "6.10.0", "7.0.0"):
            with self.subTest(version=version):
                data = copy.deepcopy(self.data)
                data["candidate"] = {
                    "version": version,
                    "semantic_ref": "UNFROZEN",
                    "review": {"state": "NOT_RUN", "evidence_ref": "NONE"},
                    "ratification": {"state": "NOT_REQUESTED", "evidence_ref": "NONE"},
                    "public_source_ref": "UNAVAILABLE",
                    "recovery_ref": "UNAVAILABLE",
                }
                self.assertEqual(release_state.validate_release_state(data), [])

    def test_terminal_cutover_and_next_candidate_are_legal_state_transitions(self) -> None:
        data = copy.deepcopy(self.data)
        data["historical"]["6.4.0"] = copy.deepcopy(data["accepted_current"])
        candidate = "a" * 40
        recovery = "b" * 40
        data["accepted_current"] = {
            "version": "6.5.0",
            "public_source_ref": candidate,
            "recovery_ref": recovery,
        }
        data["candidate"] = {
            "version": "6.5.0",
            "semantic_ref": candidate,
            "review": {
                "state": "PASS",
                "evidence_ref": (
                    "hjin98/scientific-software-development-protocol@"
                    + "c" * 40
                    + ":qualification/review.md"
                ),
            },
            "ratification": {
                "state": "RATIFIED",
                "evidence_ref": (
                    "hjin98/scientific-software-development-protocol@"
                    + "d" * 40
                    + ":qualification/ratification.md"
                ),
            },
            "public_source_ref": candidate,
            "recovery_ref": recovery,
        }
        self.assertEqual(release_state.validate_release_state(data), [])

        for version in ("6.5.1", "6.6.0", "7.0.0"):
            successor = copy.deepcopy(data)
            successor["candidate"] = {
                "version": version,
                "semantic_ref": "UNFROZEN",
                "review": {"state": "NOT_RUN", "evidence_ref": "NONE"},
                "ratification": {"state": "NOT_REQUESTED", "evidence_ref": "NONE"},
                "public_source_ref": "UNAVAILABLE",
                "recovery_ref": "UNAVAILABLE",
            }
            with self.subTest(next_successor=version):
                self.assertEqual(release_state.validate_release_state(successor), [])

    def test_historical_state_cannot_duplicate_accepted_current_version(self) -> None:
        data = copy.deepcopy(self.data)
        data["historical"]["6.4.0"] = {
            "public_source_ref": data["accepted_current"]["public_source_ref"],
            "recovery_ref": data["accepted_current"]["recovery_ref"],
        }
        errors = release_state.validate_release_state(data)
        self.assertTrue(any("duplicates accepted_current.version" in error for error in errors))


    def test_transition_preserves_accepted_and_historical_identity(self) -> None:
        previous = copy.deepcopy(self.data)

        rewritten = copy.deepcopy(previous)
        rewritten["accepted_current"]["recovery_ref"] = "a" * 40
        errors = release_state.validate_release_transition(previous, rewritten)
        self.assertTrue(any("cannot rewrite accepted_current identity" in error for error in errors))

        deleted = copy.deepcopy(previous)
        deleted["historical"].pop("6.3.0")
        errors = release_state.validate_release_transition(previous, deleted)
        self.assertTrue(any("cannot delete historical[6.3.0]" in error for error in errors))

        changed = copy.deepcopy(previous)
        changed["historical"]["6.3.0"]["recovery_ref"] = "a" * 40
        errors = release_state.validate_release_transition(previous, changed)
        self.assertTrue(any("cannot rewrite historical[6.3.0]" in error for error in errors))

        inserted = copy.deepcopy(previous)
        inserted["historical"]["5.15.0"] = {
            "public_source_ref": "NONE",
            "recovery_ref": "a" * 40,
        }
        errors = release_state.validate_release_transition(previous, inserted)
        self.assertTrue(any("cannot add historical versions" in error for error in errors))

    def test_accepted_cutover_requires_exact_previous_candidate_and_history_transfer(self) -> None:
        previous = copy.deepcopy(self.data)
        candidate = "a" * 40
        recovery = "b" * 40
        previous["candidate"] = {
            "version": "6.5.0",
            "semantic_ref": candidate,
            "review": {
                "state": "PASS",
                "evidence_ref": (
                    "hjin98/scientific-software-development-protocol@"
                    + "c" * 40
                    + ":qualification/review.md"
                ),
            },
            "ratification": {
                "state": "RATIFIED",
                "evidence_ref": (
                    "hjin98/scientific-software-development-protocol@"
                    + "d" * 40
                    + ":qualification/ratification.md"
                ),
            },
            "public_source_ref": candidate,
            "recovery_ref": recovery,
        }

        current = copy.deepcopy(previous)
        current["historical"]["6.4.0"] = copy.deepcopy(previous["accepted_current"])
        current["accepted_current"] = {
            "version": "6.5.0",
            "public_source_ref": candidate,
            "recovery_ref": recovery,
        }
        self.assertEqual(
            release_state.validate_release_transition(previous, current),
            [],
        )

        missing_history = copy.deepcopy(current)
        missing_history["historical"].pop("6.4.0")
        errors = release_state.validate_release_transition(previous, missing_history)
        self.assertTrue(any("add exactly the previous accepted_current version" in error for error in errors))
        self.assertTrue(any("move the previous accepted_current mapping unchanged" in error for error in errors))

        mutated_history = copy.deepcopy(current)
        mutated_history["historical"]["6.4.0"]["recovery_ref"] = "e" * 40
        errors = release_state.validate_release_transition(previous, mutated_history)
        self.assertTrue(any("move the previous accepted_current mapping unchanged" in error for error in errors))

        wrong_accepted = copy.deepcopy(current)
        wrong_accepted["accepted_current"]["recovery_ref"] = "e" * 40
        errors = release_state.validate_release_transition(previous, wrong_accepted)
        self.assertTrue(any("must equal the previous candidate recovery" in error for error in errors))

        incomplete = copy.deepcopy(previous)
        incomplete["candidate"]["review"] = {"state": "NOT_RUN", "evidence_ref": "NONE"}
        errors = release_state.validate_release_transition(incomplete, current)
        self.assertTrue(any("requires previous candidate Review PASS" in error for error in errors))

    def test_recovery_lineage_rejects_real_stale_p6_for_p7(self) -> None:
        errors: list[str] = []
        release_state._check_recovery_lineage(
            ROOT,
            "6.5.0",
            "133c747a1f9ab4372c9e1af7a7e9666316dc892b",
            "NONE",
            "NONE",
            "133c747a1f9ab4372c9e1af7a7e9666316dc892b",
            "dd06da8136416e67644586c44880b466f982b8ff",
            errors,
        )
        self.assertTrue(any("recovery_ref lineage" in error for error in errors))

    def test_recovery_lineage_requires_complete_pre_mapping_snapshot(self) -> None:
        candidate = "a" * 40
        review_commit = "b" * 40
        ratification_commit = "c" * 40
        recovery = "d" * 40
        review_evidence = (
            "hjin98/scientific-software-development-protocol@"
            + review_commit
            + ":qualification/review.md"
        )
        ratification_evidence = (
            "hjin98/scientific-software-development-protocol@"
            + ratification_commit
            + ":qualification/ratification.md"
        )
        complete_snapshot = f"""schema_version: 1
project: hjin98/scientific-software-development-protocol
accepted_current:
  version: "6.4.0"
  public_source_ref: {"e" * 40}
  recovery_ref: {"f" * 40}
historical: {{}}
candidate:
  version: "6.5.0"
  semantic_ref: {candidate}
  review:
    state: PASS
    evidence_ref: {review_evidence}
  ratification:
    state: RATIFIED
    evidence_ref: {ratification_evidence}
  public_source_ref: {candidate}
  recovery_ref: UNAVAILABLE
"""
        with (
            mock.patch.object(
                release_state,
                "_canonical_is_ancestor",
                return_value=True,
            ),
            mock.patch.object(
                release_state,
                "_git",
                return_value=(0, complete_snapshot),
            ),
        ):
            errors: list[str] = []
            release_state._check_recovery_lineage(
                ROOT,
                "6.5.0",
                candidate,
                review_evidence,
                ratification_evidence,
                candidate,
                recovery,
                errors,
            )
        self.assertEqual(errors, [])

        stale_snapshot = complete_snapshot.replace("state: RATIFIED", "state: NOT_REQUESTED")
        with (
            mock.patch.object(
                release_state,
                "_canonical_is_ancestor",
                return_value=True,
            ),
            mock.patch.object(
                release_state,
                "_git",
                return_value=(0, stale_snapshot),
            ),
        ):
            errors = []
            release_state._check_recovery_lineage(
                ROOT,
                "6.5.0",
                candidate,
                review_evidence,
                ratification_evidence,
                candidate,
                recovery,
                errors,
            )
        self.assertTrue(any("later immutable target" in error for error in errors))


    def _run_topology_git(
        self,
        root: Path,
        *args: str,
        env: dict[str, str] | None = None,
    ) -> str:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        return result.stdout.strip()

    def _init_topology_repo(self, root: Path) -> None:
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        self._run_topology_git(root, "config", "user.email", "ssdp-test@example.com")
        self._run_topology_git(root, "config", "user.name", "SSDP Test")

    def _topology_state(
        self,
        marker: str,
        *,
        protected_history: bool = False,
    ) -> dict:
        data = copy.deepcopy(self.data)
        data["candidate"] = {
            "version": "6.5.0",
            "semantic_ref": marker * 40,
            "review": {"state": "NOT_RUN", "evidence_ref": "NONE"},
            "ratification": {"state": "NOT_REQUESTED", "evidence_ref": "NONE"},
            "public_source_ref": "UNAVAILABLE",
            "recovery_ref": "UNAVAILABLE",
        }
        if protected_history:
            data["historical"]["6.3.5"] = {
                "public_source_ref": "5" * 40,
                "recovery_ref": "6" * 40,
            }
        else:
            data["historical"].pop("6.3.5", None)
        return data

    def _write_topology_state(self, root: Path, data: dict) -> None:
        (root / "PROTOCOL-RELEASE-STATE.yaml").write_text(
            yaml.safe_dump(data, sort_keys=False),
            encoding="utf-8",
        )

    def _commit_topology_repo(
        self,
        root: Path,
        message: str,
        *,
        date: str | None = None,
    ) -> str:
        self._run_topology_git(root, "add", "-A")
        env = None
        if date is not None:
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = date
            env["GIT_COMMITTER_DATE"] = date
        self._run_topology_git(root, "commit", "-m", message, env=env)
        return self._run_topology_git(root, "rev-parse", "HEAD")

    def test_previous_governed_states_use_head_for_working_tree_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)
            previous = self._topology_state("a")
            self._write_topology_state(root, previous)
            self._commit_topology_repo(root, "previous")

            current = self._topology_state("b")
            self._write_topology_state(root, current)
            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                root,
                current,
                errors,
            )
            self.assertEqual(errors, [])
            self.assertEqual(states, [previous])

    def test_previous_governed_states_use_linear_parent_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)
            previous = self._topology_state("a")
            self._write_topology_state(root, previous)
            self._commit_topology_repo(root, "previous")

            current = self._topology_state("b")
            self._write_topology_state(root, current)
            self._commit_topology_repo(root, "current")

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                root,
                current,
                errors,
            )
            self.assertEqual(errors, [])
            self.assertEqual(states, [previous])

    def test_previous_governed_states_cross_evidence_only_descendants(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)
            previous = self._topology_state("a")
            self._write_topology_state(root, previous)
            self._commit_topology_repo(root, "previous")

            current = self._topology_state("b")
            self._write_topology_state(root, current)
            self._commit_topology_repo(root, "transition")
            (root / "evidence.txt").write_text("evidence\n", encoding="utf-8")
            self._commit_topology_repo(root, "evidence only")

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                root,
                current,
                errors,
            )
            self.assertEqual(errors, [])
            self.assertEqual(states, [previous])

    def test_previous_governed_states_cover_date_reordered_merge_parents(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)
            base = self._topology_state("a")
            self._write_topology_state(root, base)
            base_ref = self._commit_topology_repo(
                root,
                "base",
                date="2026-01-01T00:00:00+00:00",
            )

            self._run_topology_git(root, "checkout", "-q", "-b", "governed")
            governed = self._topology_state("b", protected_history=True)
            self._write_topology_state(root, governed)
            governed_ref = self._commit_topology_repo(
                root,
                "governed parent",
                date="2026-01-02T00:00:00+00:00",
            )

            self._run_topology_git(
                root,
                "checkout",
                "-q",
                "-b",
                "sibling",
                base_ref,
            )
            sibling = self._topology_state("c")
            self._write_topology_state(root, sibling)
            sibling_ref = self._commit_topology_repo(
                root,
                "later-dated sibling",
                date="2026-01-03T00:00:00+00:00",
            )

            current = self._topology_state("d")
            self._write_topology_state(root, current)
            self._run_topology_git(root, "add", "PROTOCOL-RELEASE-STATE.yaml")
            tree_ref = self._run_topology_git(root, "write-tree")
            merge_ref = self._run_topology_git(
                root,
                "commit-tree",
                tree_ref,
                "-p",
                governed_ref,
                "-p",
                sibling_ref,
                "-m",
                "synthetic merge",
            )
            self._run_topology_git(root, "reset", "--hard", merge_ref)

            governed_time = int(
                self._run_topology_git(
                    root,
                    "show",
                    "-s",
                    "--format=%ct",
                    governed_ref,
                )
            )
            sibling_time = int(
                self._run_topology_git(
                    root,
                    "show",
                    "-s",
                    "--format=%ct",
                    sibling_ref,
                )
            )
            self.assertGreater(sibling_time, governed_time)

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                root,
                current,
                errors,
            )
            self.assertEqual(errors, [])
            self.assertEqual(len(states), 2)
            self.assertIn(governed, states)
            self.assertIn(sibling, states)

            results = [
                release_state.validate_release_transition(previous, current)
                for previous in states
            ]
            self.assertTrue(any(result == [] for result in results))
            self.assertTrue(
                any(
                    any(
                        "cannot delete historical[6.3.5]" in error
                        for error in result
                    )
                    for result in results
                )
            )

    def test_previous_governed_states_deduplicate_equivalent_merge_lineages(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)
            previous = self._topology_state("a")
            self._write_topology_state(root, previous)
            previous_ref = self._commit_topology_repo(root, "previous")

            self._run_topology_git(root, "checkout", "-q", "-b", "left")
            current = self._topology_state("b")
            self._write_topology_state(root, current)
            left_ref = self._commit_topology_repo(root, "left")

            self._run_topology_git(
                root,
                "checkout",
                "-q",
                "-b",
                "right",
                previous_ref,
            )
            self._write_topology_state(root, current)
            right_ref = self._commit_topology_repo(root, "right")
            tree_ref = self._run_topology_git(
                root,
                "rev-parse",
                f"{left_ref}^{{tree}}",
            )
            merge_ref = self._run_topology_git(
                root,
                "commit-tree",
                tree_ref,
                "-p",
                left_ref,
                "-p",
                right_ref,
                "-m",
                "equivalent merge",
            )
            self._run_topology_git(root, "reset", "--hard", merge_ref)

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                root,
                current,
                errors,
            )
            self.assertEqual(errors, [])
            self.assertEqual(states, [previous])

    def test_previous_governed_states_handle_synthetic_pr_merge(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)
            (root / "base.txt").write_text("base\n", encoding="utf-8")
            base_ref = self._commit_topology_repo(root, "pre-owner base")

            self._run_topology_git(root, "checkout", "-q", "-b", "feature")
            previous = self._topology_state("a")
            self._write_topology_state(root, previous)
            self._commit_topology_repo(root, "introduce release state")

            current = self._topology_state("b")
            self._write_topology_state(root, current)
            feature_ref = self._commit_topology_repo(root, "feature transition")
            tree_ref = self._run_topology_git(
                root,
                "rev-parse",
                f"{feature_ref}^{{tree}}",
            )
            merge_ref = self._run_topology_git(
                root,
                "commit-tree",
                tree_ref,
                "-p",
                base_ref,
                "-p",
                feature_ref,
                "-m",
                "pull request merge",
            )
            self._run_topology_git(root, "reset", "--hard", merge_ref)

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                root,
                current,
                errors,
            )
            self.assertEqual(errors, [])
            self.assertEqual(states, [previous])


    def _build_deleted_owner_merge(
        self,
        root: Path,
        *,
        reverse_parents: bool = False,
        reverse_dates: bool = False,
        absent_commits: int = 1,
    ) -> tuple[dict, dict]:
        base = self._topology_state("a")
        self._write_topology_state(root, base)
        base_ref = self._commit_topology_repo(
            root,
            "governed base",
            date="2026-01-01T00:00:00+00:00",
        )

        self._run_topology_git(root, "checkout", "-q", "-b", "good")
        current = self._topology_state("b")
        self._write_topology_state(root, current)
        good_ref = self._commit_topology_repo(
            root,
            "good current",
            date=(
                "2026-01-04T00:00:00+00:00"
                if reverse_dates
                else "2026-01-02T00:00:00+00:00"
            ),
        )

        self._run_topology_git(
            root,
            "checkout",
            "-q",
            "-b",
            "deleted",
            base_ref,
        )
        (root / "PROTOCOL-RELEASE-STATE.yaml").unlink()
        deleted_ref = self._commit_topology_repo(
            root,
            "delete governed owner",
            date=(
                "2026-01-02T00:00:00+00:00"
                if reverse_dates
                else "2026-01-03T00:00:00+00:00"
            ),
        )
        for index in range(1, absent_commits):
            (root / f"absent-{index}.txt").write_text(
                f"still absent {index}\n",
                encoding="utf-8",
            )
            deleted_ref = self._commit_topology_repo(
                root,
                f"owner still absent {index}",
            )

        tree_ref = self._run_topology_git(
            root,
            "rev-parse",
            f"{good_ref}^{{tree}}",
        )
        parents = [good_ref, deleted_ref]
        if reverse_parents:
            parents.reverse()
        args = ["commit-tree", tree_ref]
        for parent in parents:
            args.extend(["-p", parent])
        args.extend(["-m", "restore owner by merge"])
        merge_ref = self._run_topology_git(root, *args)
        self._run_topology_git(root, "reset", "--hard", merge_ref)
        return base, current

    def test_previous_governed_states_reject_deleted_owner_merge_lineage(self) -> None:
        for reverse_parents in (False, True):
            for reverse_dates in (False, True):
                with self.subTest(
                    reverse_parents=reverse_parents,
                    reverse_dates=reverse_dates,
                ):
                    with tempfile.TemporaryDirectory() as tmpdir:
                        root = Path(tmpdir)
                        self._init_topology_repo(root)
                        previous, current = self._build_deleted_owner_merge(
                            root,
                            reverse_parents=reverse_parents,
                            reverse_dates=reverse_dates,
                        )

                        errors: list[str] = []
                        states = release_state._previous_governed_release_states(
                            root,
                            current,
                            errors,
                        )
                        self.assertEqual(states, [previous])
                        self.assertTrue(
                            any(
                                "owner deletion/reintroduction cannot be treated as pre-owner ancestry"
                                in error
                                for error in errors
                            )
                        )

    def test_previous_governed_states_reject_long_owner_absence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)
            previous, current = self._build_deleted_owner_merge(
                root,
                absent_commits=4,
            )

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                root,
                current,
                errors,
            )
            self.assertEqual(states, [previous])
            self.assertTrue(
                any(
                    "owner deletion/reintroduction cannot be treated as pre-owner ancestry"
                    in error
                    for error in errors
                )
            )

    def test_previous_governed_states_reject_same_lineage_reintroduction(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)
            previous = self._topology_state("a")
            self._write_topology_state(root, previous)
            self._commit_topology_repo(root, "governed state")

            (root / "PROTOCOL-RELEASE-STATE.yaml").unlink()
            self._commit_topology_repo(root, "delete owner")

            current = self._topology_state("b")
            self._write_topology_state(root, current)
            self._commit_topology_repo(root, "reintroduce owner")

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                root,
                current,
                errors,
            )
            self.assertEqual(states, [])
            self.assertTrue(
                any(
                    "owner deletion/reintroduction cannot be treated as pre-owner ancestry"
                    in error
                    for error in errors
                )
            )

    def test_previous_governed_states_allow_long_genuine_pre_owner_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)
            for index in range(3):
                (root / f"pre-owner-{index}.txt").write_text(
                    f"pre-owner {index}\n",
                    encoding="utf-8",
                )
                base_ref = self._commit_topology_repo(
                    root,
                    f"pre-owner {index}",
                )

            self._run_topology_git(root, "checkout", "-q", "-b", "feature")
            previous = self._topology_state("a")
            self._write_topology_state(root, previous)
            self._commit_topology_repo(root, "introduce release state")
            current = self._topology_state("b")
            self._write_topology_state(root, current)
            feature_ref = self._commit_topology_repo(root, "feature transition")

            tree_ref = self._run_topology_git(
                root,
                "rev-parse",
                f"{feature_ref}^{{tree}}",
            )
            merge_ref = self._run_topology_git(
                root,
                "commit-tree",
                tree_ref,
                "-p",
                base_ref,
                "-p",
                feature_ref,
                "-m",
                "long pre-owner pull request merge",
            )
            self._run_topology_git(root, "reset", "--hard", merge_ref)

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                root,
                current,
                errors,
            )
            self.assertEqual(errors, [])
            self.assertEqual(states, [previous])


    def test_previous_governed_states_fail_closed_on_shallow_working_tree_reintroduction(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            shallow = Path(tmpdir) / "shallow"
            source.mkdir()
            self._init_topology_repo(source)

            (source / "pre-owner.txt").write_text("pre-owner\n", encoding="utf-8")
            self._commit_topology_repo(source, "pre-owner")

            previous = self._topology_state("a")
            self._write_topology_state(source, previous)
            self._commit_topology_repo(source, "introduce governed owner")

            (source / "PROTOCOL-RELEASE-STATE.yaml").unlink()
            self._commit_topology_repo(source, "delete governed owner")

            subprocess.run(
                [
                    "git",
                    "clone",
                    "-q",
                    "--depth",
                    "1",
                    source.resolve().as_uri(),
                    str(shallow),
                ],
                check=True,
            )
            self.assertEqual(
                self._run_topology_git(
                    shallow,
                    "rev-parse",
                    "--is-shallow-repository",
                ),
                "true",
            )

            current = self._topology_state("b")
            self._write_topology_state(shallow, current)

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                shallow,
                current,
                errors,
            )
            self.assertEqual(states, [])
            self.assertTrue(
                any(
                    "cannot establish genuine pre-owner release-state ancestry"
                    in error
                    for error in errors
                )
            )

    def test_previous_governed_states_fail_closed_on_shallow_missing_merge_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            shallow = Path(tmpdir) / "shallow"
            source.mkdir()
            self._init_topology_repo(source)

            base = self._topology_state("a")
            self._write_topology_state(source, base)
            base_ref = self._commit_topology_repo(source, "governed base")

            self._run_topology_git(source, "checkout", "-q", "-b", "good")
            current = self._topology_state("b")
            self._write_topology_state(source, current)
            good_ref = self._commit_topology_repo(source, "good current")

            self._run_topology_git(
                source,
                "checkout",
                "-q",
                "-b",
                "deleted",
                base_ref,
            )
            (source / "PROTOCOL-RELEASE-STATE.yaml").unlink()
            deleted_ref = self._commit_topology_repo(
                source,
                "delete governed owner",
            )

            tree_ref = self._run_topology_git(
                source,
                "rev-parse",
                f"{good_ref}^{{tree}}",
            )
            merge_ref = self._run_topology_git(
                source,
                "commit-tree",
                tree_ref,
                "-p",
                good_ref,
                "-p",
                deleted_ref,
                "-m",
                "restore owner by merge",
            )
            self._run_topology_git(source, "reset", "--hard", merge_ref)

            subprocess.run(
                [
                    "git",
                    "clone",
                    "-q",
                    "--depth",
                    "2",
                    source.resolve().as_uri(),
                    str(shallow),
                ],
                check=True,
            )
            self.assertEqual(
                self._run_topology_git(
                    shallow,
                    "rev-parse",
                    "--is-shallow-repository",
                ),
                "true",
            )

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                shallow,
                current,
                errors,
            )
            self.assertEqual(states, [])
            self.assertTrue(
                any(
                    "cannot establish genuine pre-owner release-state ancestry"
                    in error
                    for error in errors
                )
            )

    def test_previous_governed_states_allow_working_tree_first_owner_introduction(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)
            (root / "pre-owner.txt").write_text("pre-owner\n", encoding="utf-8")
            self._commit_topology_repo(root, "pre-owner")

            current = self._topology_state("b")
            self._write_topology_state(root, current)

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                root,
                current,
                errors,
            )
            self.assertEqual(errors, [])
            self.assertEqual(states, [])

    def test_previous_governed_states_reject_working_tree_reintroduction(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)
            previous = self._topology_state("a")
            self._write_topology_state(root, previous)
            self._commit_topology_repo(root, "governed state")

            (root / "PROTOCOL-RELEASE-STATE.yaml").unlink()
            self._commit_topology_repo(root, "delete owner")

            current = self._topology_state("b")
            self._write_topology_state(root, current)

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                root,
                current,
                errors,
            )
            self.assertEqual(states, [])
            self.assertTrue(
                any(
                    "owner deletion/reintroduction cannot be treated as pre-owner ancestry"
                    in error
                    for error in errors
                )
            )


    def test_previous_governed_states_fail_closed_on_unreadable_historical_owner_objects(self) -> None:
        for missing_object in ("blob", "tree"):
            with self.subTest(missing_object=missing_object):
                with tempfile.TemporaryDirectory() as tmpdir:
                    root = Path(tmpdir)
                    self._init_topology_repo(root)

                    (root / "pre-owner.txt").write_text(
                        "pre-owner\n",
                        encoding="utf-8",
                    )
                    self._commit_topology_repo(root, "pre-owner")

                    previous = self._topology_state("a")
                    self._write_topology_state(root, previous)
                    owner_ref = self._commit_topology_repo(
                        root,
                        "introduce governed owner",
                    )
                    if missing_object == "blob":
                        object_ref = self._run_topology_git(
                            root,
                            "rev-parse",
                            f"{owner_ref}:PROTOCOL-RELEASE-STATE.yaml",
                        )
                    else:
                        object_ref = self._run_topology_git(
                            root,
                            "rev-parse",
                            f"{owner_ref}^{{tree}}",
                        )

                    (root / "PROTOCOL-RELEASE-STATE.yaml").unlink()
                    self._commit_topology_repo(root, "delete governed owner")

                    git_dir_text = self._run_topology_git(
                        root,
                        "rev-parse",
                        "--git-dir",
                    )
                    git_dir = Path(git_dir_text)
                    if not git_dir.is_absolute():
                        git_dir = root / git_dir
                    object_path = (
                        git_dir
                        / "objects"
                        / object_ref[:2]
                        / object_ref[2:]
                    )
                    self.assertTrue(object_path.is_file())
                    object_path.unlink()

                    self.assertEqual(
                        self._run_topology_git(
                            root,
                            "rev-parse",
                            "--is-shallow-repository",
                        ),
                        "false",
                    )

                    current = self._topology_state("b")
                    self._write_topology_state(root, current)

                    errors: list[str] = []
                    states = release_state._previous_governed_release_states(
                        root,
                        current,
                        errors,
                    )
                    self.assertEqual(states, [])
                    self.assertTrue(
                        any(
                            "cannot establish genuine pre-owner release-state ancestry"
                            in error
                            for error in errors
                        )
                    )

    def test_previous_governed_states_use_canonical_ancestry_under_replace_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)

            (root / "pre-owner.txt").write_text("pre-owner\n", encoding="utf-8")
            pre_ref = self._commit_topology_repo(root, "pre-owner")

            previous = self._topology_state("a")
            self._write_topology_state(root, previous)
            self._commit_topology_repo(root, "introduce governed owner")

            (root / "PROTOCOL-RELEASE-STATE.yaml").unlink()
            deleted_ref = self._commit_topology_repo(root, "delete governed owner")
            tree_ref = self._run_topology_git(
                root,
                "rev-parse",
                f"{deleted_ref}^{{tree}}",
            )
            replacement_ref = self._run_topology_git(
                root,
                "commit-tree",
                tree_ref,
                "-p",
                pre_ref,
                "-m",
                "replacement hides governed owner",
            )
            self._run_topology_git(
                root,
                "replace",
                deleted_ref,
                replacement_ref,
            )
            self.assertEqual(
                self._run_topology_git(
                    root,
                    "rev-list",
                    "--full-history",
                    "HEAD",
                    "--",
                    "PROTOCOL-RELEASE-STATE.yaml",
                ),
                "",
            )

            current = self._topology_state("b")
            self._write_topology_state(root, current)

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                root,
                current,
                errors,
            )
            self.assertEqual(states, [])
            self.assertTrue(
                any(
                    "owner deletion/reintroduction cannot be treated as pre-owner ancestry"
                    in error
                    for error in errors
                )
            )

    def test_previous_governed_states_use_canonical_ancestry_under_graft(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)

            (root / "pre-owner.txt").write_text("pre-owner\n", encoding="utf-8")
            pre_ref = self._commit_topology_repo(root, "pre-owner")

            previous = self._topology_state("a")
            self._write_topology_state(root, previous)
            self._commit_topology_repo(root, "introduce governed owner")

            (root / "PROTOCOL-RELEASE-STATE.yaml").unlink()
            deleted_ref = self._commit_topology_repo(root, "delete governed owner")

            git_dir_text = self._run_topology_git(
                root,
                "rev-parse",
                "--git-dir",
            )
            git_dir = Path(git_dir_text)
            if not git_dir.is_absolute():
                git_dir = root / git_dir
            grafts = git_dir / "info" / "grafts"
            grafts.parent.mkdir(parents=True, exist_ok=True)
            grafts.write_text(
                f"{deleted_ref} {pre_ref}\n",
                encoding="utf-8",
            )

            current = self._topology_state("b")
            self._write_topology_state(root, current)

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                root,
                current,
                errors,
            )
            self.assertEqual(states, [])
            self.assertTrue(
                any(
                    "owner deletion/reintroduction cannot be treated as pre-owner ancestry"
                    in error
                    for error in errors
                )
            )

    def test_previous_governed_states_follow_readable_alternate_object_store(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            shared = Path(tmpdir) / "shared"
            source.mkdir()
            self._init_topology_repo(source)

            (source / "pre-owner.txt").write_text("pre-owner\n", encoding="utf-8")
            self._commit_topology_repo(source, "pre-owner")

            previous = self._topology_state("a")
            self._write_topology_state(source, previous)
            self._commit_topology_repo(source, "introduce governed owner")

            (source / "PROTOCOL-RELEASE-STATE.yaml").unlink()
            self._commit_topology_repo(source, "delete governed owner")

            subprocess.run(
                [
                    "git",
                    "clone",
                    "-q",
                    "--shared",
                    str(source),
                    str(shared),
                ],
                check=True,
            )

            current = self._topology_state("b")
            self._write_topology_state(shared, current)

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                shared,
                current,
                errors,
            )
            self.assertEqual(states, [])
            self.assertTrue(
                any(
                    "owner deletion/reintroduction cannot be treated as pre-owner ancestry"
                    in error
                    for error in errors
                )
            )


    def _build_sibling_commits(self, root: Path) -> tuple[str, str, str]:
        (root / "base.txt").write_text("base\n", encoding="utf-8")
        base_ref = self._commit_topology_repo(root, "base")

        self._run_topology_git(root, "checkout", "-q", "-b", "left")
        (root / "left.txt").write_text("left\n", encoding="utf-8")
        left_ref = self._commit_topology_repo(root, "left")

        self._run_topology_git(root, "checkout", "-q", "-b", "right", base_ref)
        (root / "right.txt").write_text("right\n", encoding="utf-8")
        right_ref = self._commit_topology_repo(root, "right")
        return base_ref, left_ref, right_ref

    def test_check_ancestor_uses_canonical_parents_under_replace_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)
            _, left_ref, right_ref = self._build_sibling_commits(root)

            tree_ref = self._run_topology_git(
                root,
                "rev-parse",
                f"{right_ref}^{{tree}}",
            )
            replacement_ref = self._run_topology_git(
                root,
                "commit-tree",
                tree_ref,
                "-p",
                left_ref,
                "-m",
                "replacement makes sibling look ancestral",
            )
            self._run_topology_git(root, "replace", right_ref, replacement_ref)

            self.assertEqual(
                self._run_topology_git(
                    root,
                    "merge-base",
                    "--is-ancestor",
                    left_ref,
                    right_ref,
                ),
                "",
            )

            errors: list[str] = []
            release_state._check_ancestor(
                root,
                left_ref,
                right_ref,
                "replacement-overlay lineage",
                errors,
            )
            self.assertTrue(
                any(
                    "replacement-overlay lineage requires" in error
                    for error in errors
                )
            )

    def test_check_ancestor_uses_canonical_parents_under_graft(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)
            _, left_ref, right_ref = self._build_sibling_commits(root)

            git_dir_text = self._run_topology_git(
                root,
                "rev-parse",
                "--git-dir",
            )
            git_dir = Path(git_dir_text)
            if not git_dir.is_absolute():
                git_dir = root / git_dir
            grafts = git_dir / "info" / "grafts"
            grafts.parent.mkdir(parents=True, exist_ok=True)
            grafts.write_text(
                f"{right_ref} {left_ref}\n",
                encoding="utf-8",
            )

            self.assertEqual(
                self._run_topology_git(
                    root,
                    "merge-base",
                    "--is-ancestor",
                    left_ref,
                    right_ref,
                ),
                "",
            )

            errors: list[str] = []
            release_state._check_ancestor(
                root,
                left_ref,
                right_ref,
                "graft-overlay lineage",
                errors,
            )
            self.assertTrue(
                any(
                    "graft-overlay lineage requires" in error
                    for error in errors
                )
            )

    def test_recovery_lineage_rejects_replace_rewritten_sibling(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)

            (root / "base.txt").write_text("base\n", encoding="utf-8")
            base_ref = self._commit_topology_repo(root, "base")

            self._run_topology_git(root, "checkout", "-q", "-b", "semantic")
            (root / "semantic.txt").write_text("semantic\n", encoding="utf-8")
            semantic_ref = self._commit_topology_repo(root, "semantic candidate")

            self._run_topology_git(
                root,
                "checkout",
                "-q",
                "-b",
                "recovery",
                base_ref,
            )
            recovery_state = copy.deepcopy(self.data)
            recovery_state["candidate"] = {
                "version": "6.5.0",
                "semantic_ref": semantic_ref,
                "review": {"state": "PASS", "evidence_ref": "NONE"},
                "ratification": {"state": "RATIFIED", "evidence_ref": "NONE"},
                "public_source_ref": semantic_ref,
                "recovery_ref": "UNAVAILABLE",
            }
            self._write_topology_state(root, recovery_state)
            recovery_ref = self._commit_topology_repo(root, "sibling recovery")

            tree_ref = self._run_topology_git(
                root,
                "rev-parse",
                f"{recovery_ref}^{{tree}}",
            )
            replacement_ref = self._run_topology_git(
                root,
                "commit-tree",
                tree_ref,
                "-p",
                semantic_ref,
                "-m",
                "replacement launders recovery ancestry",
            )
            self._run_topology_git(
                root,
                "replace",
                recovery_ref,
                replacement_ref,
            )
            self.assertEqual(
                self._run_topology_git(
                    root,
                    "merge-base",
                    "--is-ancestor",
                    semantic_ref,
                    recovery_ref,
                ),
                "",
            )

            errors: list[str] = []
            release_state._check_recovery_lineage(
                root,
                "6.5.0",
                semantic_ref,
                "NONE",
                "NONE",
                semantic_ref,
                recovery_ref,
                errors,
            )
            self.assertTrue(
                any(
                    "candidate.recovery_ref lineage requires" in error
                    for error in errors
                )
            )
            self.assertFalse(
                any("later immutable target" in error for error in errors)
            )

    def test_review_evidence_reads_canonical_commit_under_replace_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)
            candidate = "a" * 40
            evidence_path = Path("qualification") / "review.md"
            (root / evidence_path).parent.mkdir(parents=True, exist_ok=True)
            (root / evidence_path).write_text(
                f"---\nstatus: pass\ncandidate_ref: {candidate}\n---\n# Review\n",
                encoding="utf-8",
            )
            evidence_commit = self._commit_topology_repo(root, "canonical evidence")

            (root / evidence_path).write_text(
                f"---\nstatus: no-pass\ncandidate_ref: {'b' * 40}\n---\n# Forged\n",
                encoding="utf-8",
            )
            forged_commit = self._commit_topology_repo(root, "replacement evidence")
            self._run_topology_git(
                root,
                "replace",
                evidence_commit,
                forged_commit,
            )

            errors: list[str] = []
            release_state._check_review_evidence(
                root,
                "hjin98/scientific-software-development-protocol",
                "hjin98/scientific-software-development-protocol@"
                + evidence_commit
                + ":qualification/review.md",
                candidate,
                "PASS",
                "candidate.review.evidence_ref",
                errors,
            )
            self.assertEqual(errors, [])

    def test_previous_governed_states_reject_laundered_reintroduction_after_later_transition(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_topology_repo(root)

            first = self._topology_state("a")
            self._write_topology_state(root, first)
            self._commit_topology_repo(root, "governed A")

            (root / "PROTOCOL-RELEASE-STATE.yaml").unlink()
            self._commit_topology_repo(root, "delete governed owner")

            reintroduced = self._topology_state("b")
            self._write_topology_state(root, reintroduced)
            self._commit_topology_repo(root, "reintroduce as B")

            current = self._topology_state("c")
            self._write_topology_state(root, current)
            self._commit_topology_repo(root, "later material C")
            (root / "evidence.txt").write_text("evidence only\n", encoding="utf-8")
            self._commit_topology_repo(root, "later evidence only")

            errors: list[str] = []
            states = release_state._previous_governed_release_states(
                root,
                current,
                errors,
            )
            self.assertEqual(states, [reintroduced])
            self.assertTrue(
                any(
                    "hidden by a later material transition"
                    in error
                    for error in errors
                )
            )



if __name__ == "__main__":
    unittest.main()
