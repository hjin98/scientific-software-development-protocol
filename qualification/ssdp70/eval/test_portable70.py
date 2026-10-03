import json
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

import core70
import harness70
from adapters import claude


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


class ProjectStagingTests(unittest.TestCase):
    def test_history_hard_links_are_refused_before_copy_or_chmod(self):
        for copied_collision in (False, True):
            with self.subTest(copied_collision=copied_collision), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                fixture = root / "corpus/fixtures/frozen"
                source = fixture / "project"
                source.mkdir(parents=True)
                outside = root / "outside.txt"
                outside.write_text("protected\n")
                outside.chmod(0o400)
                if copied_collision:
                    (source / "history-data").write_text("overlay\n")
                (fixture / "build_history.sh").write_text(
                    f'ln "{outside}" history-data\n'
                )
                project = root / "working"
                with self.assertRaisesRegex(core70.ContractError, "hard-linked file: history-data"):
                    harness70.build_project(
                        root / "corpus", {"id": "E1", "fixture": "frozen"}, project, []
                    )
                self.assertEqual(stat.S_IMODE(outside.stat().st_mode), 0o400)
                self.assertEqual(outside.read_text(), "protected\n")
                self.assertFalse((project / ".git").exists())

    def test_history_git_commits_and_restricted_modes_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = root / "corpus/fixtures/frozen"
            source = fixture / "project"
            nested = source / "nested"
            nested.mkdir(parents=True)
            data = nested / "data.txt"
            data.write_text("frozen\n")
            executable = source / "run.sh"
            executable.write_text("#!/bin/sh\nprintf staged\n")
            data.chmod(0o440)
            executable.chmod(0o551)
            nested.chmod(0o550)
            source.chmod(0o550)
            (fixture / "build_history.sh").write_text(
                "git init -q\nprintf history > historical.txt\ngit add historical.txt\n"
                "git -c user.email=eval@example.invalid -c user.name=eval commit -qm history\n"
            )
            project = root / "working"
            try:
                harness70.build_project(root / "corpus", {"id": "E1", "fixture": "frozen"}, project, [".omp"])
                self.assertEqual(subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=project), b"2\n")
                self.assertEqual(subprocess.check_output(["git", "status", "--porcelain"], cwd=project), b"")
                self.assertEqual((project / ".git/info/exclude").read_text(), harness70.project_git_exclude([".omp"]))
                self.assertEqual(stat.S_IMODE((project / "nested").stat().st_mode), 0o750)
                self.assertEqual(stat.S_IMODE((project / "nested/data.txt").stat().st_mode), 0o640)
                self.assertEqual(stat.S_IMODE((project / "run.sh").stat().st_mode), 0o751)
                self.assertEqual(subprocess.check_output([str(project / "run.sh")]), b"staged")
                (project / "nested/data.txt").write_text("edited\n")
                self.assertEqual(data.read_text(), "frozen\n")
                self.assertEqual(stat.S_IMODE(data.stat().st_mode), 0o440)
                self.assertEqual(stat.S_IMODE(executable.stat().st_mode), 0o551)
                self.assertEqual(stat.S_IMODE(nested.stat().st_mode), 0o550)
                self.assertEqual(stat.S_IMODE(source.stat().st_mode), 0o550)
            finally:
                source.chmod(0o700)
                nested.chmod(0o700)

    def test_frozen_fixture_becomes_writable_without_changing_custody(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "corpus" / "fixtures" / "frozen" / "project"
            nested = source / "nested"
            nested.mkdir(parents=True)
            data = nested / "data.txt"
            data.write_text("frozen data\n")
            executable = source / "run.sh"
            executable.write_text("#!/bin/sh\nprintf staged\n")
            data.chmod(0o400)
            executable.chmod(0o500)
            nested.chmod(0o500)
            source.chmod(0o500)
            before = {p: (stat.S_IMODE(p.stat().st_mode), p.read_bytes() if p.is_file() else None)
                      for p in (source, nested, data, executable)}
            project = root / "working"
            try:
                harness70.build_project(root / "corpus", {"id": "E1", "fixture": "frozen"}, project, [])
                self.assertEqual(stat.S_IMODE(project.stat().st_mode), 0o700)
                self.assertEqual(stat.S_IMODE((project / "nested").stat().st_mode), 0o700)
                self.assertEqual(stat.S_IMODE((project / "nested/data.txt").stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE((project / "run.sh").stat().st_mode), 0o700)
                self.assertEqual(subprocess.check_output(["git", "status", "--porcelain"], cwd=project), b"")
                self.assertEqual(subprocess.check_output([str(project / "run.sh")], cwd=project), b"staged")
                (project / "nested/data.txt").write_text("edited\n")
                (project / "nested/new.txt").write_text("created\n")
                self.assertTrue(subprocess.check_output(["git", "diff", "--", "nested/data.txt"], cwd=project))
                for path, expected in before.items():
                    self.assertEqual((stat.S_IMODE(path.stat().st_mode), path.read_bytes() if path.is_file() else None), expected)
            finally:
                # Only the synthetic fixture needs thawing for temporary cleanup.
                source.chmod(0o700)
                nested.chmod(0o700)

    def test_staging_does_not_chmod_history_script_symlink_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = root / "corpus/fixtures/frozen"
            (fixture / "project").mkdir(parents=True)
            outside = root / "outside.txt"
            outside.write_text("protected\n")
            outside.chmod(0o400)
            outside_dir = root / "outside-dir"
            outside_dir.mkdir()
            (outside_dir / "data.txt").write_text("protected\n")
            (outside_dir / "data.txt").chmod(0o400)
            (fixture / "build_history.sh").write_text(
                f'ln -s "{outside}" file-link\nln -s "{outside_dir}" dir-link\n'
            )
            harness70.build_project(root / "corpus", {"id": "E1", "fixture": "frozen"}, root / "working", [])
            self.assertEqual(stat.S_IMODE(outside.stat().st_mode), 0o400)
            self.assertEqual(stat.S_IMODE((outside_dir / "data.txt").stat().st_mode), 0o400)


class PortableCoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.profile = self.root / "profile.json"
        self.capabilities = self.root / "capabilities.json"
        write_json(self.capabilities, {
            "schema": 1,
            "capabilities": {
                name: {"decision": "ALLOW" if name not in {"delegation", "network_remote_service"} else "DENY", "scope": "*"}
                for name in core70.REQUIRED_CAPABILITY_CLASSES
            },
            "native_capabilities": {
                "tool:Read": {"semantic_classes": ["workspace_read_search_list"], "scope": "test read"}
            },
        })
        write_json(self.profile, {
            "schema": 1,
            "profile_id": "test-profile",
            "adapter_id": claude.ADAPTER_ID,
            "agent_model": "test-model",
            "provider_runtime": {"provider": "test", "runtime": "claude-code", "executable": "claude", "version": "exposed-v1"},
            "reasoning_configuration": {"effort": "high"},
            "workspace_realization": {"kind": "tempdir"},
            "install_mechanism": "project-skills",
            "budgets": {"max_turns": 60, "timeout_s": 3600},
            "containment_policy": {"kind": "external-pre-effect"},
            "network_external_write_policy": {"network": "deny", "external_write": "sandbox"},
            "credential_service_account_policy": {"ambient_credentials": "deny"},
            "provider_managed_unknowns": [
                {"name": "backend-shard", "classification": "arm-neutral", "sensitive_claims": ["*"]}
            ],
            "native_tools": ["Read"],
            "native_surface_requirements": [],
            "mcp_servers": [],
        })

    def tearDown(self):
        self.tmp.cleanup()

    def requirements(self):
        req = self.root / "req"
        req.mkdir(exist_ok=True)
        write_json(req / "required_artifacts.json", {"schema": 1, "episodes": {"E1": ["final-report.md", "trace.jsonl"]}})
        write_json(req / "required_oracles.json", {"schema": 1, "episodes": {"E1": [{"id": "o1", "path": "check_o1.py"}]}})
        write_json(req / "expected_scoring_items.json", {"schema": 1, "episodes": {"E1": [
            {"id": "i1", "measure": "critical-judgment", "critical": True, "branch": "main", "allowed_dispositions": ["pass", "fail", "unresolved"]},
            {"id": "i2", "measure": "null-coverage", "critical": False, "branch": "main", "allowed_dispositions": ["pass", "fail", "unresolved", "not-applicable"]},
        ]}})
        return core70.load_requirements(req, "E1")

    def write_admission(
        self,
        role="executor",
        omit=None,
        *,
        include_section6=True,
        omit_section6_cell=None,
        extra_section6_cell=None,
        section6_status="PASS",
        corrupt_section6_sha=False,
        status="ADMITTED",
        subdir=None,
    ):
        bundle = core70.load_profile(self.profile, self.capabilities)
        dir_name = subdir or f"{role}-admission"
        root = self.root / dir_name
        evidence = root / "evidence"
        evidence.mkdir(parents=True, exist_ok=True)
        names = core70.EXECUTOR_ADMISSION_CHECKS if role == "executor" else core70.EVALUATOR_ADMISSION_CHECKS
        checks = {}
        for name in names:
            if name == omit:
                continue
            artifact = evidence / f"{name}.json"
            artifact.write_text(json.dumps({"check": name, "pass": True}), encoding="utf-8")
            checks[name] = {
                "status": "PASS",
                "evidence_path": f"evidence/{name}.json",
                "evidence_sha256": core70.sha256_file(artifact),
            }
        payload = {
            "schema": 1,
            "status": status,
            "role": role,
            "profile_key_sha256": bundle.profile_key_sha256,
            "adapter_sha256": "adapter-a",
            "core_sha256": "core-a",
            "capability_manifest_sha256": bundle.capability_manifest_sha256,
            "checks": checks,
        }
        if role == "executor" and include_section6:
            s6_evidence = root / "section6_evidence"
            s6_evidence.mkdir(parents=True, exist_ok=True)
            s6_cells = {}
            for cell_name in core70.EXECUTOR_SECTION6_CELLS:
                if cell_name == omit_section6_cell:
                    continue
                art = s6_evidence / f"{cell_name}.json"
                art.write_text(json.dumps({"cell": cell_name, "pass": True}), encoding="utf-8")
                actual_sha = core70.sha256_file(art)
                s6_cells[cell_name] = {
                    "status": section6_status,
                    "evidence_path": f"section6_evidence/{cell_name}.json",
                    "evidence_sha256": "0" * 64 if corrupt_section6_sha else actual_sha,
                }
            if extra_section6_cell:
                extra_art = s6_evidence / f"{extra_section6_cell}.json"
                extra_art.write_text(json.dumps({"cell": extra_section6_cell}), encoding="utf-8")
                s6_cells[extra_section6_cell] = {
                    "status": "PASS",
                    "evidence_path": f"section6_evidence/{extra_section6_cell}.json",
                    "evidence_sha256": core70.sha256_file(extra_art),
                }
            payload["section6"] = s6_cells
        admission = root / "admission.json"
        write_json(admission, payload)
        return admission, bundle

    def test_profile_key_changes_with_material_capability_change(self):
        a = core70.load_profile(self.profile, self.capabilities)
        caps = json.loads(self.capabilities.read_text())
        caps["capabilities"]["process_execution"]["decision"] = "DENY"
        write_json(self.capabilities, caps)
        b = core70.load_profile(self.profile, self.capabilities)
        self.assertNotEqual(a.profile_key_sha256, b.profile_key_sha256)

    def test_uncontrolled_provider_unknown_fails_sensitive_claim(self):
        profile = json.loads(self.profile.read_text())
        profile["provider_managed_unknowns"] = [
            {"name": "hidden-system-prompt", "classification": "uncontrolled", "sensitive_claims": ["owner-read"]}
        ]
        write_json(self.profile, profile)
        bundle = core70.load_profile(self.profile, self.capabilities)
        self.assertTrue(core70.profile_claim_errors(bundle, ["owner-read"]))
        self.assertFalse(core70.profile_claim_errors(bundle, ["timing"]))

    def test_admission_requires_exact_check_set_and_hashed_evidence(self):
        admission, bundle = self.write_admission()
        self.assertEqual(core70.validate_profile_admission(
            admission, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
        ), [])
        incomplete, bundle = self.write_admission(omit=core70.EXECUTOR_ADMISSION_CHECKS[-1], subdir="incomplete-checks")
        errors = core70.validate_profile_admission(
            incomplete, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
        )
        self.assertTrue(any("missing required checks" in error for error in errors))

    def test_admission_rejects_tampered_proof_artifact(self):
        admission, bundle = self.write_admission(subdir="tampered-check-proof")
        proof = admission.parent / "evidence" / f"{core70.EXECUTOR_ADMISSION_CHECKS[0]}.json"
        proof.write_text("tampered", encoding="utf-8")
        errors = core70.validate_profile_admission(
            admission, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
        )
        self.assertTrue(any("hash does not match" in error for error in errors))

    def test_admission_snapshot_preserves_and_validates_all_proofs(self):
        admission, _ = self.write_admission(subdir="snapshot-valid")
        out = self.root / "run-admission"
        out.mkdir()
        bundle_sha = core70.admission_bundle_sha256(admission, role="executor")
        snapshot = core70.snapshot_profile_admission(admission, out, role="executor")
        self.assertIn("section6_proofs", snapshot)
        self.assertEqual(len(snapshot["proofs"]), len(core70.EXECUTOR_ADMISSION_CHECKS))
        self.assertEqual(len(snapshot["section6_proofs"]), len(core70.EXECUTOR_SECTION6_CELLS))
        self.assertEqual(core70.validate_profile_admission_snapshot(
            out, bundle_sha, role="executor"), [])
        proof = out / "profile-admission-evidence" / f"{core70.EXECUTOR_ADMISSION_CHECKS[0]}.proof"
        proof.write_text("tampered", encoding="utf-8")
        self.assertTrue(core70.validate_profile_admission_snapshot(
            out, bundle_sha, role="executor"))

    def test_admission_rejects_missing_section6_matrix_for_executor(self):
        # Local-compliance/global-failure counterexample:
        # An ADMITTED executor record containing only EXECUTOR_ADMISSION_CHECKS and no section6 field
        # must now be rejected in qualification mode.
        admission, bundle = self.write_admission(include_section6=False, subdir="no-section6")
        errors = core70.validate_profile_admission(
            admission, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
        )
        self.assertTrue(any("section6 matrix is missing" in err for err in errors), errors)
        with self.assertRaises(core70.ContractError) as ctx:
            core70.admission_bundle_sha256(admission, role="executor")
        self.assertIn("section6 matrix is missing", str(ctx.exception))

    def test_admission_rejects_missing_or_unknown_section6_cell(self):
        missing_cell = core70.EXECUTOR_SECTION6_CELLS[3]
        admission_missing, bundle = self.write_admission(
            omit_section6_cell=missing_cell, subdir="missing-s6-cell"
        )
        errors = core70.validate_profile_admission(
            admission_missing, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
        )
        self.assertTrue(any(f"missing required cells: ['{missing_cell}']" in err for err in errors), errors)

        admission_unknown, bundle = self.write_admission(
            extra_section6_cell="unknown_extra_cell", subdir="unknown-s6-cell"
        )
        errors = core70.validate_profile_admission(
            admission_unknown, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
        )
        self.assertTrue(any("unknown cells: ['unknown_extra_cell']" in err for err in errors), errors)

    def test_admission_rejects_non_pass_section6_cell_status(self):
        for bad_status in ("PENDING", "FAIL", "UNRESOLVED"):
            admission, bundle = self.write_admission(
                section6_status=bad_status, subdir=f"s6-status-{bad_status}"
            )
            errors = core70.validate_profile_admission(
                admission, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
                adapter_sha256="adapter-a", core_sha256="core-a",
                capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
            )
            self.assertTrue(
                any("section6 cell 'known_broken_both_arms_miss' did not PASS" in err for err in errors),
                f"expected PASS failure for {bad_status}, got: {errors}",
            )

    def test_admission_rejects_missing_corrupt_or_tampered_section6_evidence(self):
        cell_name = core70.EXECUTOR_SECTION6_CELLS[0]

        # Missing evidence artifact
        admission_missing, bundle = self.write_admission(subdir="s6-missing-evidence")
        art = admission_missing.parent / "section6_evidence" / f"{cell_name}.json"
        art.unlink()
        errors = core70.validate_profile_admission(
            admission_missing, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
        )
        self.assertTrue(any("evidence is unavailable" in err for err in errors), errors)

        # Corrupt evidence SHA
        admission_corrupt, bundle = self.write_admission(
            corrupt_section6_sha=True, subdir="s6-corrupt-sha"
        )
        errors = core70.validate_profile_admission(
            admission_corrupt, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
        )
        self.assertTrue(any("evidence hash does not match" in err for err in errors), errors)

        # Tampered evidence after admission construction
        admission_tampered, bundle = self.write_admission(subdir="s6-tampered-evidence")
        tamper_art = admission_tampered.parent / "section6_evidence" / f"{cell_name}.json"
        tamper_art.write_text("tampered content", encoding="utf-8")
        errors = core70.validate_profile_admission(
            admission_tampered, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
        )
        self.assertTrue(any("evidence hash does not match" in err for err in errors), errors)

    def test_admission_bundle_sha_commits_to_section6_proofs(self):
        admission, _ = self.write_admission(subdir="s6-bundle-sha")
        sha_initial = core70.admission_bundle_sha256(admission, role="executor")
        cell_name = core70.EXECUTOR_SECTION6_CELLS[5]
        art = admission.parent / "section6_evidence" / f"{cell_name}.json"
        art.write_text("altered content", encoding="utf-8")
        sha_altered = core70.admission_bundle_sha256(admission, role="executor")
        self.assertNotEqual(sha_initial, sha_altered)

    def test_snapshot_preserves_and_validates_section6_proofs_and_fails_closed_on_tamper(self):
        admission, _ = self.write_admission(subdir="s6-snapshot-test")
        out = self.root / "run-s6-snapshot"
        out.mkdir()
        bundle_sha = core70.admission_bundle_sha256(admission, role="executor")
        snapshot = core70.snapshot_profile_admission(admission, out, role="executor")

        # Snapshot contains both complete ordinary-check and §6 proof sets
        self.assertEqual({p["check"] for p in snapshot["proofs"]}, set(core70.EXECUTOR_ADMISSION_CHECKS))
        self.assertEqual({p["cell"] for p in snapshot["section6_proofs"]}, set(core70.EXECUTOR_SECTION6_CELLS))
        self.assertEqual(core70.validate_profile_admission_snapshot(out, bundle_sha, role="executor"), [])

        # Tampered §6 proof in snapshot
        target_cell = core70.EXECUTOR_SECTION6_CELLS[2]
        s6_proof = out / "profile-admission-evidence" / f"section6-{target_cell}.proof"
        s6_proof.write_text("tampered proof content", encoding="utf-8")
        errors = core70.validate_profile_admission_snapshot(out, bundle_sha, role="executor")
        self.assertTrue(any(f"section6 proof '{target_cell}' hash changed" in err for err in errors), errors)

        # Missing §6 proof in snapshot
        s6_proof.unlink()
        errors = core70.validate_profile_admission_snapshot(out, bundle_sha, role="executor")
        self.assertTrue(any(f"section6 proof '{target_cell}' is unavailable" in err for err in errors), errors)

    def test_snapshot_rejects_coherent_rebinding_tamper_of_section6_proof(self):
        admission, _ = self.write_admission(subdir="s6-rebinding-test")
        out = self.root / "run-s6-rebinding"
        out.mkdir()
        bundle_sha = core70.admission_bundle_sha256(admission, role="executor")
        core70.snapshot_profile_admission(admission, out, role="executor")

        # Snapshot is initially completely valid and matches run identity
        self.assertEqual(core70.validate_profile_admission_snapshot(out, bundle_sha, role="executor"), [])
        self.assertEqual(core70.recompute_profile_admission_snapshot_bundle_sha256(out, role="executor"), bundle_sha)

        # Attack: Coherent rebinding of one Section 6 proof
        target_cell = core70.EXECUTOR_SECTION6_CELLS[0]
        s6_proof = out / "profile-admission-evidence" / f"section6-{target_cell}.proof"
        s6_proof.write_text("coherently altered section6 proof content", encoding="utf-8")
        new_sha = core70.sha256_file(s6_proof)
        new_size = s6_proof.stat().st_size

        # 1. Update evidence_sha256 in the archived admission record
        record_file = out / "profile-admission.json"
        record = json.loads(record_file.read_text(encoding="utf-8"))
        record["section6"][target_cell]["evidence_sha256"] = new_sha
        write_json(record_file, record)

        # 2. Update snapshot proof SHA/size
        snapshot_file = out / "profile-admission-snapshot.json"
        snapshot = json.loads(snapshot_file.read_text(encoding="utf-8"))
        for row in snapshot["section6_proofs"]:
            if row.get("cell") == target_cell:
                row["sha256"] = new_sha
                row["bytes"] = new_size

        # 3. Update record_sha256 in snapshot
        snapshot["record_sha256"] = core70.sha256_file(record_file)

        # 4. Leave snapshot["admission_bundle_sha256"] untouched (still equals bundle_sha)
        self.assertEqual(snapshot["admission_bundle_sha256"], bundle_sha)
        write_json(snapshot_file, snapshot)

        # Verify all local metadata checks would pass in isolation
        self.assertEqual(core70.sha256_file(record_file), snapshot["record_sha256"])
        self.assertEqual(core70.sha256_file(s6_proof), new_sha)
        self.assertEqual(record["section6"][target_cell]["evidence_sha256"], new_sha)

        # But validate_profile_admission_snapshot MUST reject because recomputed bundle digest differs
        errors = core70.validate_profile_admission_snapshot(out, bundle_sha, role="executor")
        self.assertTrue(any("recomputed bundle does not match run identity" in err for err in errors), errors)
        self.assertTrue(any("snapshot bundle does not match recomputed digest" in err for err in errors), errors)
        self.assertNotEqual(
            core70.recompute_profile_admission_snapshot_bundle_sha256(out, role="executor"),
            bundle_sha,
        )

    def test_snapshot_rejects_coherent_rebinding_tamper_of_ordinary_check_proof(self):
        admission, _ = self.write_admission(subdir="check-rebinding-test")
        out = self.root / "run-check-rebinding"
        out.mkdir()
        bundle_sha = core70.admission_bundle_sha256(admission, role="executor")
        core70.snapshot_profile_admission(admission, out, role="executor")

        # Snapshot is initially completely valid
        self.assertEqual(core70.validate_profile_admission_snapshot(out, bundle_sha, role="executor"), [])

        # Attack: Coherent rebinding of an ordinary executor check proof
        target_check = core70.EXECUTOR_ADMISSION_CHECKS[0]
        check_proof = out / "profile-admission-evidence" / f"{target_check}.proof"
        check_proof.write_text("coherently altered ordinary check proof content", encoding="utf-8")
        new_sha = core70.sha256_file(check_proof)
        new_size = check_proof.stat().st_size

        # 1. Update evidence_sha256 in the archived admission record
        record_file = out / "profile-admission.json"
        record = json.loads(record_file.read_text(encoding="utf-8"))
        record["checks"][target_check]["evidence_sha256"] = new_sha
        write_json(record_file, record)

        # 2. Update snapshot proof SHA/size
        snapshot_file = out / "profile-admission-snapshot.json"
        snapshot = json.loads(snapshot_file.read_text(encoding="utf-8"))
        for row in snapshot["proofs"]:
            if row.get("check") == target_check:
                row["sha256"] = new_sha
                row["bytes"] = new_size

        # 3. Update record_sha256 in snapshot
        snapshot["record_sha256"] = core70.sha256_file(record_file)

        # 4. Leave snapshot["admission_bundle_sha256"] untouched
        self.assertEqual(snapshot["admission_bundle_sha256"], bundle_sha)
        write_json(snapshot_file, snapshot)

        # Recomputed bundle digest must reject the coherently rebound archive
        errors = core70.validate_profile_admission_snapshot(out, bundle_sha, role="executor")
        self.assertTrue(any("recomputed bundle does not match run identity" in err for err in errors), errors)
        self.assertTrue(any("snapshot bundle does not match recomputed digest" in err for err in errors), errors)
        self.assertNotEqual(
            core70.recompute_profile_admission_snapshot_bundle_sha256(out, role="executor"),
            bundle_sha,
        )

    def test_snapshot_rejects_coherent_rebinding_tamper_for_evaluator_role(self):
        eval_admission, _ = self.write_admission(role="evaluator", subdir="eval-rebinding-test")
        out = self.root / "eval-snap-rebinding"
        out.mkdir()
        bundle_sha = core70.admission_bundle_sha256(eval_admission, role="evaluator")
        core70.snapshot_profile_admission(eval_admission, out, role="evaluator")

        self.assertEqual(core70.validate_profile_admission_snapshot(out, bundle_sha, role="evaluator"), [])

        target_check = core70.EVALUATOR_ADMISSION_CHECKS[0]
        check_proof = out / "profile-admission-evidence" / f"{target_check}.proof"
        check_proof.write_text("coherently altered evaluator check proof content", encoding="utf-8")
        new_sha = core70.sha256_file(check_proof)
        new_size = check_proof.stat().st_size

        record_file = out / "profile-admission.json"
        record = json.loads(record_file.read_text(encoding="utf-8"))
        record["checks"][target_check]["evidence_sha256"] = new_sha
        write_json(record_file, record)

        snapshot_file = out / "profile-admission-snapshot.json"
        snapshot = json.loads(snapshot_file.read_text(encoding="utf-8"))
        for row in snapshot["proofs"]:
            if row.get("check") == target_check:
                row["sha256"] = new_sha
                row["bytes"] = new_size
        snapshot["record_sha256"] = core70.sha256_file(record_file)
        self.assertEqual(snapshot["admission_bundle_sha256"], bundle_sha)
        write_json(snapshot_file, snapshot)

        errors = core70.validate_profile_admission_snapshot(out, bundle_sha, role="evaluator")
        self.assertTrue(any("recomputed bundle does not match run identity" in err for err in errors), errors)
        self.assertTrue(any("snapshot bundle does not match recomputed digest" in err for err in errors), errors)
        self.assertNotEqual(
            core70.recompute_profile_admission_snapshot_bundle_sha256(out, role="evaluator"),
            bundle_sha,
        )

    def test_candidate_to_admitted_record_with_incomplete_section6_rejected(self):
        # Candidate record promoted to ADMITTED status but with incomplete §6 cell
        admission, bundle = self.write_admission(
            status="ADMITTED",
            omit_section6_cell=core70.EXECUTOR_SECTION6_CELLS[1],
            subdir="candidate-promoted-incomplete-s6",
        )
        errors = core70.validate_profile_admission(
            admission, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
        )
        self.assertTrue(any("missing required cells" in err for err in errors), errors)

        # Complete evidence with status=CANDIDATE rejected by qualification mode
        candidate_admission, bundle = self.write_admission(
            status="CANDIDATE", subdir="complete-candidate"
        )
        errors = core70.validate_profile_admission(
            candidate_admission, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
        )
        self.assertTrue(any("status does not match current realization" in err for err in errors), errors)

    def test_evaluator_admission_remains_unaffected_by_section6(self):
        eval_admission, bundle = self.write_admission(role="evaluator", subdir="eval-admission")
        # Evaluator has no section6 and validates cleanly
        self.assertEqual(core70.validate_profile_admission(
            eval_admission, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="evaluator",
        ), [])
        out = self.root / "eval-snap"
        out.mkdir()
        bundle_sha = core70.admission_bundle_sha256(eval_admission, role="evaluator")
        snap = core70.snapshot_profile_admission(eval_admission, out, role="evaluator")
        self.assertNotIn("section6_proofs", snap)
        self.assertEqual(core70.validate_profile_admission_snapshot(out, bundle_sha, role="evaluator"), [])

    def test_probe_mode_does_not_require_admission_record(self):
        self.assertEqual(core70.validate_profile_admission(
            None, mode="probe", profile_key_sha256="k", adapter_sha256="a", core_sha256="c",
            capability_manifest_sha256="m", role="executor",
        ), [])

    def test_runtime_observation_rejects_unfrozen_or_mismatched_runtime(self):
        bundle = core70.load_profile(self.profile, self.capabilities)
        self.assertEqual(core70.validate_runtime_observation(
            bundle, {"model": "test-model", "runtime_version": "exposed-v1", "tools": ["Read"], "native_capabilities": [], "memory_paths": {}, "mcp_servers": []}), [])
        self.assertTrue(core70.validate_runtime_observation(
            bundle, {"model": "test-model", "runtime_version": "other", "tools": ["Read"], "native_capabilities": [], "memory_paths": {}, "mcp_servers": []}))
        profile = json.loads(self.profile.read_text())
        profile["provider_runtime"]["version"] = "MUST-BE-FROZEN-BEFORE-QUALIFICATION"
        write_json(self.profile, profile)
        frozen = core70.load_profile(self.profile, self.capabilities)
        self.assertTrue(core70.validate_runtime_observation(
            frozen, {"model": "test-model", "runtime_version": "x", "tools": ["Read"], "native_capabilities": [], "memory_paths": {}, "mcp_servers": []}))

    def test_scoring_exact_closure_rejects_empty_and_duplicates(self):
        req = self.requirements()
        self.assertTrue(core70.validate_dispositions([], req))
        valid = [
            {"item": "i1", "measure": "critical-judgment", "critical": True, "result": "pass"},
            {"item": "i2", "measure": "null-coverage", "critical": False, "result": "not-applicable"},
        ]
        self.assertEqual(core70.validate_dispositions(valid, req), [])
        self.assertTrue(core70.validate_dispositions(valid + [dict(valid[0])], req))

    def test_required_oracle_hashes_are_enforced(self):
        req = self.requirements()
        run = self.root / "run"
        run.mkdir()
        (run / "final-report.md").write_text("x")
        (run / "trace.jsonl").write_text("{}\n")
        (run / "o1.out").write_text("ok")
        (run / "o1.err").write_text("")
        write_json(run / "oracle.json", {"schema": 1, "results": {"o1": {
            "executed": True,
            "stdout_artifact": "o1.out",
            "stderr_artifact": "o1.err",
            "stdout_sha256": core70.sha256_file(run / "o1.out"),
            "stderr_sha256": core70.sha256_file(run / "o1.err"),
        }}})
        self.assertEqual(core70.validate_required_oracles(run, req), [])
        (run / "o1.out").write_text("changed")
        self.assertEqual(core70.validate_required_oracles(run, req), ["o1"])

    def test_requirements_snapshot_is_content_bound(self):
        req = self.requirements()
        snapshot = core70.requirements_snapshot(req)
        parsed = core70.requirements_from_snapshot(snapshot, snapshot["manifest_digests"])
        self.assertEqual(parsed, req)
        snapshot["expected_scoring_items"][0]["measure"] = "tampered"
        with self.assertRaises(core70.ContractError):
            core70.requirements_from_snapshot(snapshot, snapshot["manifest_digests"])

    def test_event_payload_schema_rejects_missing_result_evidence(self):
        event = {
            "schema_version": 1, "run_id": "r", "event_id": "e1", "sequence": 1,
            "actor_id": "executor", "kind": "resource_access",
            "native_source": {"native_index": 0, "native_sha256": "a" * 64},
            "status": "result", "timing": None,
            "payload": {
                "operation": "read", "resource_identity": "/x", "input": {}, "tool_use_id": "t1",
                "result_status": "result", "result_reference": None, "result_sha256": None,
                "resolved_package_identity": None, "resource_sha256": None, "resource_bytes": None,
            },
        }
        errors = core70.validate_normalized_events([event], "r")
        self.assertTrue(any("result_reference" in error for error in errors))

    def test_termination_requires_portable_boolean_is_error(self):
        missing_flag = [{
            "schema_version": 1, "run_id": "r", "event_id": "e000001", "sequence": 1,
            "actor_id": "executor", "kind": "termination",
            "native_source": {"native_index": 0, "native_sha256": "a" * 64},
            "status": "observed", "timing": None,
            "payload": {"state": "error", "native_return_state": {"isError": True}, "terminal_result_exists": False},
        }]
        errors = core70.validate_normalized_events(missing_flag, "r")
        self.assertTrue(any("native_return_state.is_error" in error for error in errors), errors)
        self.assertEqual(harness70._termination_state(missing_flag), (True, False))

        success = [{
            "kind": "termination",
            "payload": {"state": "completed", "native_return_state": {"is_error": False}, "terminal_result_exists": True},
        }]
        failure = [{
            "kind": "termination",
            "payload": {"state": "error", "native_return_state": {"is_error": True}, "terminal_result_exists": False},
        }]
        self.assertEqual(harness70._termination_state(success), (True, True))
        self.assertEqual(harness70._termination_state(failure), (True, False))

    def test_normalization_completeness_rejects_dropped_event(self):
        events = [{
            "schema_version": 1, "run_id": "r", "event_id": "e000001", "sequence": 1,
            "actor_id": "executor", "kind": "termination",
            "native_source": {"native_index": 1, "native_sha256": "a" * 64},
            "status": "observed", "timing": None,
            "payload": {"state": "completed", "native_return_state": {"is_error": False}, "terminal_result_exists": True},
        }]
        mapping = [{"native_index": 1, "native_sha256": "a" * 64, "mapped_event_ids": ["e000001"], "classification": "terminal", "oracle_relevant": True}]
        errors = core70.validate_completeness_map(2, mapping, events)
        self.assertTrue(any("missing from completeness map" in error for error in errors))


class ClaudeAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.skills = self.root / ".claude" / "skills"
        owner = self.skills / "software-implementation" / "references" / "scientific-inspectability-and-initiative.md"
        owner.parent.mkdir(parents=True)
        owner.write_text("owner bytes", encoding="utf-8")
        skill = self.skills / "software-implementation" / "SKILL.md"
        skill.write_text("# root", encoding="utf-8")
        self.context = {
            "project": str(self.root),
            "skills_root": str(self.skills),
            "package_identity": {
                "arm": "p70", "commit": "abc", "version": "7.0.0",
                "package_sha256": "b" * 64,
            },
        }

    def tearDown(self):
        self.tmp.cleanup()

    def test_full_owner_read_has_success_result_and_exact_resource_bytes(self):
        owner = self.skills / "software-implementation" / "references" / "scientific-inspectability-and-initiative.md"
        stdout = "\n".join([
            json.dumps({"type": "system", "subtype": "init", "skills": sorted(claude.SSDP_SKILLS), "model": "m", "claude_code_version": "v1"}),
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "u1", "name": "Read", "input": {"file_path": str(owner)}}
            ]}}),
            json.dumps({"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "u1", "content": "owner bytes", "is_error": False}
            ]}}),
            json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "done", "duration_ms": 1, "usage": {}}),
        ])
        events, mapping, errors, native_count = claude.normalize(stdout, "run-1", self.context)
        self.assertEqual(errors, [])
        self.assertEqual(core70.validate_normalized_events(events, "run-1"), [])
        self.assertEqual(core70.validate_completeness_map(native_count, mapping, events), [])
        self.assertTrue(claude.owner_reads(events, "scientific-inspectability-and-initiative.md"))
        result = [e for e in events if e["kind"] == "resource_access" and e["status"] == "result"][0]
        self.assertEqual(result["payload"]["resource_bytes"], len(b"owner bytes"))
        self.assertIsNotNone(result["payload"]["resource_sha256"])

    def test_ordinary_entry_root_is_observed_from_skill_read(self):
        skill = self.skills / "software-implementation" / "SKILL.md"
        stdout = "\n".join([
            json.dumps({"type": "system", "subtype": "init", "skills": sorted(claude.SSDP_SKILLS), "model": "m", "claude_code_version": "v1"}),
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "u1", "name": "Read", "input": {"file_path": str(skill)}}
            ]}}),
            json.dumps({"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "u1", "content": "# root", "is_error": False}
            ]}}),
            json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "done", "duration_ms": 1, "usage": {}}),
        ])
        events, _, errors, _ = claude.normalize(stdout, "run-2", self.context)
        self.assertEqual(errors, [])
        roots = [e for e in events if e["kind"] == "root_selection"]
        self.assertTrue(any(e["payload"]["selection_mechanism"] == "ordinary-resource-read" for e in roots))

    def test_missing_tool_result_is_fail_closed(self):
        stdout = "\n".join([
            json.dumps({"type": "system", "subtype": "init", "skills": sorted(claude.SSDP_SKILLS), "model": "m", "claude_code_version": "v1"}),
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "u1", "name": "Read", "input": {"file_path": str(self.skills / "software-implementation" / "SKILL.md")}}
            ]}}),
            json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "done", "duration_ms": 1, "usage": {}}),
        ])
        _, _, errors, _ = claude.normalize(stdout, "run-3", self.context)
        self.assertTrue(any("no exposed tool result" in error for error in errors))

    def test_unknown_native_event_type_is_fail_closed(self):
        stdout = json.dumps({"type": "mystery", "payload": {"x": 1}})
        _, mapping, errors, native_count = claude.normalize(stdout, "run-4", self.context)
        self.assertTrue(errors)
        self.assertEqual(native_count, 1)
        self.assertTrue(mapping[0]["oracle_relevant"])


class EvidenceStateTests(unittest.TestCase):
    def test_incomplete_terminal_cannot_be_complete(self):
        state, reasons = core70.run_evidence_state(
            execution_ok=True, profile_errors=[], event_errors=[], completeness_errors=[],
            catalog_ok=True, terminal_exists=False, final_result_exists=False,
            missing_artifacts=[], missing_oracles=[])
        self.assertEqual(state, "MISSING_REQUIRED_EVIDENCE")
        self.assertTrue(reasons)

    def test_execution_transport_success_does_not_override_inadmissible_profile(self):
        state, _ = core70.run_evidence_state(
            execution_ok=True, profile_errors=["uncontrolled hidden state"], event_errors=[], completeness_errors=[],
            catalog_ok=True, terminal_exists=True, final_result_exists=True,
            missing_artifacts=[], missing_oracles=[])
        self.assertEqual(state, "INADMISSIBLE")


if __name__ == "__main__":
    unittest.main()
