"""Focused unit tests for the OMP Stage 7 target-host campaign driver."""
import base64
import html
import json
import shlex
import sys
import tempfile
import unittest

import yaml
from pathlib import Path
from unittest import mock
from urllib.parse import quote_from_bytes, quote_plus

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import core70  # noqa: E402
import omp_stage7_admission as admission  # noqa: E402
import omp_stage7_campaign as driver  # noqa: E402


class Stage7CampaignDriverTests(unittest.TestCase):
    def _campaign(self, root: Path) -> Path:
        camp = root / "admission" / "campaign"
        camp.mkdir(parents=True)
        (camp / "proofs").mkdir()
        value = {
            "schema": admission.SCHEMA,
            "kind": admission.KIND,
            "state": "CANDIDATE_EVIDENCE",
            "candidate_head": "a" * 40,
            "semantic_subject": driver.SEMANTIC_SUBJECT_DEFAULT,
            "profile": {
                "profile_key_sha256": "1" * 64,
                "profile_document_sha256": "2" * 64,
                "capability_manifest_sha256": "3" * 64,
                "adapter_sha256": "4" * 64,
                "core_sha256": "5" * 64,
                "harness_sha256": "6" * 64,
                "adapter_support_sha256": {},
            },
            "checks": {name: {"status": "PENDING", "attempts": []}
                       for name in core70.EXECUTOR_ADMISSION_CHECKS},
            "section6": {name: {"status": "PENDING", "attempts": []}
                         for name in admission.SECTION6_CELLS},
        }
        admission._write_json(camp / "campaign.json", value)
        return camp

    def test_failed_terminal_falsification_rejects_present_error_terminal(self):
        case = driver.failed_terminal_falsification_case()
        self.assertTrue(case["terminal_exists"])
        self.assertFalse(case["terminal_ok"])
        self.assertFalse(case["execution_ok"])
        self.assertEqual(case["state"], "EXECUTION_ERROR")
        self.assertTrue(case["reasons"])
        self.assertTrue(case["terminal_event"]["payload"]["native_return_state"]["is_error"])

    def test_containment_prompt_requests_observable_denial_paths(self):
        prompt = driver.PROMPTS["S7-CONTAINMENT"]
        self.assertIn("127.0.0.1:31001", prompt)
        self.assertIn("native write tool", prompt)
        self.assertIn("/stage7-forbidden-write", prompt)

    def test_positive_episode_set_contains_every_frozen_ordinary_case(self):
        self.assertTrue(set(admission.ORDINARY_ENTRY_CASE_EPISODES.values()).issubset(driver.POSITIVE_EPISODES))
        self.assertEqual(tuple(admission.ORDINARY_ENTRY_CASE_EPISODES.values()), driver.ORDINARY_EPISODES)

    def test_prepare_corpus_is_bounded_non_custody_and_append_only(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            stagef = root / "stagef"
            admission_root = stagef / "admission"
            with mock.patch.object(admission, "STAGEF_WORKSPACE_ROOT", stagef), \
                    mock.patch.object(admission, "ADMISSION_ROOT", admission_root), \
                    mock.patch.object(driver.admission, "STAGEF_WORKSPACE_ROOT", stagef), \
                    mock.patch.object(driver.admission, "ADMISSION_ROOT", admission_root):
                camp = self._campaign(stagef)
                paths = driver.prepare_corpus(camp)
                manifest = json.loads((camp / "synthetic-corpus-manifest.json").read_text())
                self.assertTrue(manifest["non_custody"])
                self.assertFalse(manifest["blinded_protocol7_subjects_used"])
                self.assertEqual(set(manifest["episodes"]), set(driver.ALL_EPISODES))
                self.assertEqual(
                    manifest["ordinary_entry_case_classes"], admission.ORDINARY_ENTRY_CASE_EPISODES
                )
                corpus_manifest = yaml.safe_load((Path(paths["corpus"]) / "manifest.yaml").read_text())
                entries = {row["id"]: row["entry"] for row in corpus_manifest["episodes"]}
                for episode in admission.ORDINARY_ENTRY_CASE_EPISODES.values():
                    self.assertEqual(entries[episode], "ordinary")
                base_project = Path(paths["corpus"]) / "fixtures" / "base" / "project"
                required_fixture_files = {
                    "scientific_filter.py", "local_defect.py", "pipeline.py", "data.csv",
                    "analysis_report.md", "gate_results.csv", "business_report.csv", "service_test.py",
                    "architecture_note.md", "variant_history.md", "source_values.json", "rendered_values.csv",
                }
                self.assertEqual(
                    required_fixture_files,
                    {name for name in required_fixture_files if (base_project / name).is_file()},
                )
                self.assertTrue((Path(paths["corpus"]) / "fixtures" / "hostile" / "project" / ".mcp.json").is_file())
                with self.assertRaises(driver.DriverError):
                    driver.prepare_corpus(camp)

    def test_candidate_head_must_match_exact_checkout(self):
        with mock.patch.object(driver, "_repo_head", return_value="b" * 40):
            with self.assertRaises(driver.DriverError):
                driver._require_candidate_head("a" * 40)
            driver._require_candidate_head("b" * 40)

    def test_freeze_inherit_preserves_route_without_inheriting_stale_support(self):
        source_profile = {
            "adapter_id": driver.omp.ADAPTER_ID,
            "containment_policy": {"provider_route": {
                "provider_id": "deepinfra",
                "model_id": "zai-org/GLM-5.3-Flash",
                "upstream": "https://api.deepinfra.com/v1/openai",
                "api": "openai-completions",
                "base_path": "/chat",
                "context_window": 128000,
                "max_tokens": 8192,
                "reasoning": True,
            }},
            "reasoning_configuration": {"thinking": "high", "source": "--thinking"},
            "budgets": {"max_turns": 30, "timeout_s": 900},
        }
        bundle = mock.Mock(profile=source_profile, profile_key_sha256="1" * 64)
        with tempfile.TemporaryDirectory() as td, \
                mock.patch.object(driver.core70, "load_profile", return_value=bundle), \
                mock.patch.object(driver, "freeze_and_init", return_value=Path(td) / "campaign") as freeze:
            result = driver.freeze_from_source_profile(
                source_profile=Path(td) / "old-profile.json",
                source_capabilities=Path(td) / "old-capabilities.json",
                executable=Path(td) / "omp",
                capabilities=Path(td) / "cap.json",
                candidate_head="a" * 40,
                semantic_subject=driver.SEMANTIC_SUBJECT_DEFAULT,
                profile_id="new-profile",
                expected_provider_id="deepinfra",
                expected_model_id="zai-org/GLM-5.3-Flash",
                expected_upstream="https://api.deepinfra.com/v1/openai",
                expected_source_profile_key="1" * 64,
                label="test",
            )
            self.assertEqual(result, Path(td) / "campaign")
            kwargs = freeze.call_args.kwargs
            self.assertEqual(kwargs["base_path"], "/chat")
            self.assertEqual(kwargs["context_window"], 128000)
            self.assertEqual(kwargs["max_tokens"], 8192)
            self.assertEqual(kwargs["thinking"], "high")
            self.assertEqual(kwargs["max_turns"], 30)
            self.assertEqual(kwargs["timeout_s"], 900)
            self.assertNotIn("containment_policy", kwargs)

    def test_prepare_arms_materializes_exact_frozen_packages_once(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            camp = root / "campaign"
            camp.mkdir()
            def materialize(repo, commit, destination):
                destination.mkdir(parents=True)
                (destination / "skill.txt").write_text(commit + "\n", encoding="utf-8")
            digests = [
                driver.ARM_SPECS["p66"]["dist_tree_sha256"],
                driver.ARM_SPECS["p70"]["dist_tree_sha256"],
            ]
            with mock.patch.object(driver, "_campaign", return_value={}), \
                    mock.patch.object(driver, "_materialize_git_tree", side_effect=materialize), \
                    mock.patch.object(driver.core70, "sha256_tree", side_effect=digests):
                manifest = driver.prepare_arms(camp, repo=root)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual([row["name"] for row in payload["arms"]], ["p66", "p70"])
            self.assertEqual(payload["arms"][0]["commit"], driver.ARM_SPECS["p66"]["commit"])
            self.assertEqual(payload["arms"][1]["commit"], driver.SEMANTIC_SUBJECT_DEFAULT)
            with mock.patch.object(driver, "_campaign", return_value={}):
                with self.assertRaises(driver.DriverError):
                    driver.prepare_arms(camp, repo=root)

    def test_scheduler_trace_proves_sequential_arms_and_concurrent_pairs(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "scheduler.jsonl"
            rows = [
                {"schema": 1, "event": "pair_start", "pair_id": "A-r0", "order": ["p66", "p70"], "monotonic_ns": 10},
                {"schema": 1, "event": "arm_start", "pair_id": "A-r0", "arm": "p66", "monotonic_ns": 11},
                {"schema": 1, "event": "arm_end", "pair_id": "A-r0", "arm": "p66", "monotonic_ns": 20},
                {"schema": 1, "event": "arm_start", "pair_id": "A-r0", "arm": "p70", "monotonic_ns": 21},
                {"schema": 1, "event": "arm_end", "pair_id": "A-r0", "arm": "p70", "monotonic_ns": 40},
                {"schema": 1, "event": "pair_end", "pair_id": "A-r0", "monotonic_ns": 41},
                {"schema": 1, "event": "pair_start", "pair_id": "B-r0", "order": ["p70", "p66"], "monotonic_ns": 15},
                {"schema": 1, "event": "arm_start", "pair_id": "B-r0", "arm": "p70", "monotonic_ns": 16},
                {"schema": 1, "event": "arm_end", "pair_id": "B-r0", "arm": "p70", "monotonic_ns": 25},
                {"schema": 1, "event": "arm_start", "pair_id": "B-r0", "arm": "p66", "monotonic_ns": 26},
                {"schema": 1, "event": "arm_end", "pair_id": "B-r0", "arm": "p66", "monotonic_ns": 35},
                {"schema": 1, "event": "pair_end", "pair_id": "B-r0", "monotonic_ns": 36},
            ]
            path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
            self.assertEqual(driver.scheduler_trace_errors(path), [])
            rows[3]["monotonic_ns"] = 19
            path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
            self.assertTrue(any("arms overlap" in item for item in driver.scheduler_trace_errors(path)))

    def test_exact_run_requires_two_distinct_arms_and_parallel_pairs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            camp = root / "campaign"
            camp.mkdir()
            with mock.patch.object(driver, "_campaign", return_value={"profile": {"profile_key_sha256": "x"}}):
                with self.assertRaises(driver.DriverError):
                    driver.run_exact_campaign(camp, arms_manifest=root / "arms.json", arms=["p70"], parallel=2)
                with self.assertRaises(driver.DriverError):
                    driver.run_exact_campaign(camp, arms_manifest=root / "arms.json", arms=["p70", "p70"], parallel=2)
                with self.assertRaises(driver.DriverError):
                    driver.run_exact_campaign(camp, arms_manifest=root / "arms.json", arms=["p70", "p66"], parallel=1)

    def test_nonzero_child_retains_diagnostic_only_failure_evidence(self):
        with tempfile.TemporaryDirectory() as td, mock.patch.dict("os.environ", {}, clear=True):
            root = Path(td)
            log = root / "wrapper.log"
            diagnostic = root / "run" / "launch-diagnostic.json"
            argv = ["python3", "harness70.py", "episode"]
            process = mock.Mock(returncode=1, stdout=b"", stderr=b"ordinary launch failure\n")
            with mock.patch.object(driver.subprocess, "run", return_value=process):
                result = driver._run(argv, log=log, diagnostic_path=diagnostic)
            self.assertEqual(result, 1)
            self.assertFalse(log.exists())
            payload = json.loads(diagnostic.read_text(encoding="utf-8"))
            self.assertEqual(payload["kind"], "sanitized-process-failure-diagnostic")
            self.assertEqual(payload["diagnostic_status"], "EARLY_LAUNCH_FAILURE")
            self.assertEqual(payload["stderr_sanitized"], "ordinary launch failure\n")
            self.assertTrue(payload["evidence_limits"]["diagnostic_only"])
            self.assertFalse(payload["evidence_limits"]["raw_trace"])
            self.assertFalse(payload["evidence_limits"]["normalized_events"])
            self.assertFalse(payload["evidence_limits"]["terminal_event"])
            self.assertFalse(payload["evidence_limits"]["evidence_integrity_manifest"])
            self.assertFalse(payload["evidence_limits"]["complete_admissible_realization"])
            self.assertFalse(payload["evidence_limits"]["executor_admission_evidence"])
            self.assertIn("diagnostic failure evidence only", payload["note"])

    def test_episode_failure_defaults_diagnostic_to_append_only_run_directory(self):
        with tempfile.TemporaryDirectory() as td, mock.patch.dict("os.environ", {}, clear=True):
            root = Path(td)
            out = root / "out"
            profile = root / "profile.json"
            profile.write_text(json.dumps({
                "containment_policy": {"provider_route": {"credential_env": "SSDP70_OMP_PROVIDER_CREDENTIAL"}},
            }), encoding="utf-8")
            argv = [
                sys.executable, str(HERE / "harness70.py"), "episode",
                "--corpus", str(root / "corpus"), "--arms-manifest", str(root / "arms.json"),
                "--arm", "p70", "--out", str(out), "--profile", str(profile),
                "--capabilities", str(root / "capabilities.json"), "--requirements", str(root / "requirements"),
                "--adapter", "omp", "--oracles", str(root / "oracles"), "--mode", "probe",
                "--id", "E1", "--rep", "1",
            ]
            process = mock.Mock(returncode=1, stdout=b"", stderr=b"early error\n")
            with mock.patch.object(driver.subprocess, "run", return_value=process):
                self.assertEqual(driver._run(argv, log=root / "wrapper.log"), 1)
            diagnostic = out / "E1-p70-r1" / "launch-diagnostic.json"
            self.assertTrue(diagnostic.is_file())
            self.assertEqual(json.loads(diagnostic.read_text())["stderr_sanitized"], "early error\n")

    def test_finalized_nonzero_episode_keeps_existing_wrapper_log(self):
        with tempfile.TemporaryDirectory() as td, mock.patch.dict("os.environ", {}, clear=True):
            root = Path(td)
            out = root / "out"
            run = out / "E1-p70-r1"
            run.mkdir(parents=True)
            (run / "summary.json").write_text('{"evidence_state":"INADMISSIBLE"}\n', encoding="utf-8")
            profile = root / "profile.json"
            profile.write_text(json.dumps({
                "containment_policy": {"provider_route": {"credential_env": "SSDP70_OMP_PROVIDER_CREDENTIAL"}},
            }), encoding="utf-8")
            argv = [
                sys.executable, str(HERE / "harness70.py"), "episode",
                "--corpus", str(root / "corpus"), "--arms-manifest", str(root / "arms.json"),
                "--arm", "p70", "--out", str(out), "--profile", str(profile),
                "--capabilities", str(root / "capabilities.json"), "--requirements", str(root / "requirements"),
                "--adapter", "omp", "--oracles", str(root / "oracles"), "--mode", "probe",
                "--id", "E1", "--rep", "1",
            ]
            log = root / "wrapper.log"
            process = mock.Mock(returncode=2, stdout=b"finalized evidence\n", stderr=b"expected refusal\n")
            with mock.patch.object(driver.subprocess, "run", return_value=process):
                self.assertEqual(driver._run(argv, log=log), 2)
            diagnostic = run / "launch-diagnostic.json"
            self.assertEqual(
                json.loads(diagnostic.read_text(encoding="utf-8"))["diagnostic_status"],
                "FINALIZED_NONZERO_EXIT",
            )
            self.assertEqual(log.read_text(encoding="utf-8"),
                             "ARGV:\n" + json.dumps(argv) + "\n\nSTDOUT:\nfinalized evidence\n"
                             "\nSTDERR:\nexpected refusal\n")

    def test_finalized_nonzero_matrix_keeps_existing_wrapper_log(self):
        with tempfile.TemporaryDirectory() as td, mock.patch.dict("os.environ", {}, clear=True):
            root = Path(td)
            out = root / "matrix"
            out.mkdir()
            (out / "matrix-plan.json").write_text(json.dumps({
                "pairs": [{"episode_id": "E1", "rep": 0}],
            }), encoding="utf-8")
            (out / "matrix-scheduler.jsonl").write_text("\n".join([
                json.dumps({"pair_id": "E1-r0", "event": "pair_start"}),
                json.dumps({"pair_id": "E1-r0", "event": "pair_end"}),
            ]) + "\n", encoding="utf-8")
            profile = root / "profile.json"
            profile.write_text(json.dumps({
                "containment_policy": {"provider_route": {"credential_env": "SSDP70_OMP_PROVIDER_CREDENTIAL"}},
            }), encoding="utf-8")
            argv = [
                sys.executable, str(HERE / "harness70.py"), "matrix",
                "--corpus", str(root / "corpus"), "--arms-manifest", str(root / "arms.json"),
                "--arm", "p70", "--out", str(out), "--profile", str(profile),
                "--capabilities", str(root / "capabilities.json"), "--requirements", str(root / "requirements"),
                "--adapter", "omp", "--oracles", str(root / "oracles"), "--mode", "probe", "--parallel", "2",
            ]
            log = root / "wrapper.log"
            process = mock.Mock(returncode=2, stdout=b"matrix finished with unresolved runs\n", stderr=b"")
            with mock.patch.object(driver.subprocess, "run", return_value=process):
                self.assertEqual(driver._run(argv, log=log), 2)
            self.assertTrue(log.is_file())
            diagnostic = json.loads(log.with_suffix(log.suffix + ".diagnostic.json").read_text(encoding="utf-8"))
            self.assertEqual(diagnostic["diagnostic_status"], "FINALIZED_NONZERO_EXIT")

    def test_failure_diagnostic_redacts_exact_injected_credential(self):
        secret = "fixture-secret-value-that-is-not-a-real-provider-key"
        with tempfile.TemporaryDirectory() as td, mock.patch.dict(
            "os.environ", {"SSDP70_OMP_PROVIDER_CREDENTIAL": secret}, clear=True
        ):
            root = Path(td)
            diagnostic = root / "run" / "launch-diagnostic.json"
            process = mock.Mock(returncode=1, stdout=b"", stderr=f"provider rejected {secret}\n".encode())
            with mock.patch.object(driver.subprocess, "run", return_value=process):
                driver._run(["python3", "harness70.py", "episode"], log=root / "wrapper.log",
                            diagnostic_path=diagnostic)
            retained = diagnostic.read_bytes()
            self.assertNotIn(secret.encode(), retained)
            payload = json.loads(retained)
            self.assertIn("raw", payload["redacted_representations"])
            self.assertIn("provider rejected", payload["stderr_sanitized"])

    def test_failure_diagnostic_redacts_policy_encoded_credential_forms(self):
        secret = 'fixture/secret+value=<"line\\two & café\'>'
        raw = secret.encode("utf-8")
        forms = [
            secret.encode(),
            base64.b64encode(raw),
            base64.b64encode(raw).rstrip(b"="),
            base64.urlsafe_b64encode(raw),
            base64.urlsafe_b64encode(raw).rstrip(b"="),
            quote_from_bytes(raw, safe="").encode("ascii"),
            quote_plus(secret, safe="").encode("ascii"),
            ("%" + "%".join(f"{byte:02X}" for byte in raw)).encode("ascii"),
            raw.hex().encode("ascii"),
            raw.hex().upper().encode("ascii"),
            json.dumps(secret, ensure_ascii=True)[1:-1].encode("utf-8"),
            json.dumps(secret, ensure_ascii=True).encode("utf-8"),
            html.escape(secret, quote=True).encode("utf-8"),
            shlex.quote(secret).encode("utf-8"),
            secret.encode("utf-16le"),
            base64.b64encode(secret.encode("utf-16le")),
        ]
        output = b"encoded provider diagnostic:\n" + b"\n".join(forms) + b"\n"
        with tempfile.TemporaryDirectory() as td, mock.patch.dict("os.environ", {"SSDP70_OMP_PROVIDER_CREDENTIAL": secret}, clear=True):
            root = Path(td)
            diagnostic = root / "run" / "launch-diagnostic.json"
            process = mock.Mock(returncode=1, stdout=output, stderr=b"encoded form failure\n")
            with mock.patch.object(driver.subprocess, "run", return_value=process):
                driver._run(["python3", "harness70.py", "episode"], log=root / "wrapper.log",
                            diagnostic_path=diagnostic)
            retained = diagnostic.read_bytes()
            for form in forms:
                if form:
                    self.assertNotIn(form, retained)
            payload = json.loads(retained)
            self.assertTrue({"base64", "url_safe_base64", "percent_encoded", "hex_lower", "hex_upper",
                             "json_escaped", "json_quoted", "html_escaped", "shell_quoted",
                             "utf16le", "utf16le_base64"}
                            .issubset(payload["redacted_representations"]))

    def test_sanitization_failure_persists_nothing_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as td, mock.patch.dict("os.environ", {}, clear=True):
            root = Path(td)
            log = root / "wrapper.log"
            diagnostic = root / "run" / "launch-diagnostic.json"
            process = mock.Mock(returncode=1, stdout=b"ordinary stdout", stderr=b"ordinary stderr")
            with mock.patch.object(driver.subprocess, "run", return_value=process), mock.patch.object(
                driver, "_diagnostic_secret_patterns",
                side_effect=driver.DiagnosticSanitizationError("sensitive internal detail"),
            ):
                with self.assertRaisesRegex(driver.DriverError, "no output was persisted"):
                    driver._run(["python3", "harness70.py", "episode"], log=log,
                                diagnostic_path=diagnostic)
            self.assertFalse(log.exists())
            self.assertFalse(diagnostic.exists())
            self.assertEqual(list(root.rglob("*")), [])

    def test_successful_child_keeps_existing_log_format_without_diagnostic(self):
        with tempfile.TemporaryDirectory() as td, mock.patch.dict("os.environ", {}, clear=True):
            root = Path(td)
            log = root / "wrapper.log"
            diagnostic = root / "run" / "launch-diagnostic.json"
            argv = ["python3", "harness70.py", "episode"]
            process = mock.Mock(returncode=0, stdout=b"normal result\r\n", stderr=b"normal notice\r\n")
            with mock.patch.object(driver.subprocess, "run", return_value=process):
                result = driver._run(argv, log=log, diagnostic_path=diagnostic)
            expected = (
                "ARGV:\n" + json.dumps(argv) + "\n\nSTDOUT:\nnormal result\n"
                "\nSTDERR:\nnormal notice\n"
            )
            self.assertEqual(result, 0)
            self.assertEqual(log.read_text(encoding="utf-8"), expected)
            self.assertFalse(diagnostic.exists())


if __name__ == "__main__":
    unittest.main()
