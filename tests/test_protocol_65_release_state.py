from __future__ import annotations

import copy
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
        with mock.patch.object(
            release_state,
            "_git",
            side_effect=[
                (0, ""),
                (0, ""),
                (0, ""),
                (0, ""),
                (0, ""),
                (0, ""),
                (0, complete_snapshot),
            ],
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
        with mock.patch.object(
            release_state,
            "_git",
            side_effect=[
                (0, ""),
                (0, ""),
                (0, ""),
                (0, ""),
                (0, ""),
                (0, ""),
                (0, stale_snapshot),
            ],
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


if __name__ == "__main__":
    unittest.main()
