"""Unit tests for Stage 7 OMP Evaluator Adapter, Profile, and C1 Write Oracles."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
if str(EVAL_DIR) not in sys.path:
    sys.path.insert(0, str(EVAL_DIR))

import assess70
import core70
import adapters.omp_eval as omp_eval
import write_oracles


class TestOmpEvaluator(unittest.TestCase):
    """Test suite verifying evaluator adapter, profile, and C1 write oracle behavior."""

    def setUp(self):
        self.profile_path = EVAL_DIR / "profiles" / "omp-evaluator-readonly.json"
        self.cap_path = EVAL_DIR / "capabilities" / "omp-evaluator-readonly.json"

    def test_adapter_loading(self):
        adapter = assess70.load_adapter("omp_eval")
        self.assertEqual(adapter.ADAPTER_ID, "omp-eval-json-v1")
        for attr in ("ADAPTER_ID", "launch", "clean_env", "runtime_observation", "realize_containment"):
            self.assertTrue(hasattr(adapter, attr), f"Missing required adapter attribute {attr}")

    def test_profile_freeze_and_claims(self):
        bundle = core70.load_profile(self.profile_path, self.cap_path)
        self.assertIsNotNone(bundle.profile_key_sha256)
        self.assertIsNotNone(bundle.capability_manifest_sha256)
        self.assertFalse(core70._contains_unfrozen_marker(bundle.profile))
        claim_errors = core70.profile_claim_errors(bundle, [])
        self.assertEqual(claim_errors, [])

    def test_evaluator_tools_surface(self):
        bundle = core70.load_profile(self.profile_path, self.cap_path)
        self.assertEqual(bundle.profile["native_tools"], ["read", "glob", "grep"])
        self.assertEqual(bundle.profile["mcp_servers"], [])
        self.assertEqual(
            bundle.profile["workspace_realization"]["kind"],
            "temporary-read-only-evidence-bundle",
        )

    def test_stream_translation(self):
        profile = {
            "agent_model": "deepinfra/zai-org/GLM-5.3-Flash",
            "native_tools": ["read", "glob", "grep"],
            "provider_runtime": {"version": "18.0.11"},
        }
        raw_stream = "\n".join([
            json.dumps({"type": "agent_start"}),
            json.dumps({"type": "message_start", "message": {"role": "assistant"}}),
            json.dumps({"type": "content_block_delta", "delta": {"type": "text_delta", "text": "Assessment line 1\n"}}),
            json.dumps({"type": "content_block_delta", "delta": {"type": "text_delta", "text": "Assessment line 2"}}),
            json.dumps({"type": "message_end", "message": {
                "role": "assistant",
                "content": [{"type": "text", "text": "Assessment line 1\nAssessment line 2"}],
                "stopReason": "end_turn",
            }}),
            json.dumps({"type": "agent_end"}),
        ])

        translated = omp_eval.translate_stream_for_assessor(raw_stream, profile=profile, returncode=0)
        res_text, final_event = assess70.result_text(translated)
        self.assertEqual(res_text, "Assessment line 1\nAssessment line 2")
        self.assertIsNotNone(final_event)
        self.assertEqual(final_event.get("type"), "result")
        self.assertFalse(final_event.get("is_error"))

        obs = omp_eval.runtime_observation(translated)
        self.assertEqual(obs["model"], "deepinfra/zai-org/GLM-5.3-Flash")
        self.assertEqual(obs["runtime_version"], "18.0.11")
        self.assertEqual(obs["tools"], ["read", "glob", "grep"])
        self.assertEqual(obs["mcp_servers"], [])

    def test_c1_oracle_derivation_from_patch_and_headers(self):
        # Verify C1 binding: derivation from headers and diff.patch, NOT workspace_external_class or disposition
        diff_content = (
            "--- a/src/target_file.py\n"
            "+++ b/src/target_file.py\n"
            "@@ -1,3 +1,3 @@\n"
            "-old\n"
            "+new\n"
        )
        targets = write_oracles.parse_diff_patch_targets(diff_content)
        self.assertIn("src/target_file.py", targets)

        events = [
            {
                "kind": "tool_action",
                "payload": {
                    "operation": "edit",
                    "input": {"file_path": "src/target_file.py"},
                    # Intentionally poisonous fields that MUST be ignored
                    "workspace_external_class": "CORRUPTED_IGNORE_THIS",
                    "disposition": "CORRUPTED_IGNORE_THIS",
                },
            }
        ]
        derived = write_oracles.derive_targets_from_headers(events, forbid_disposition_fields=True)
        self.assertEqual(len(derived), 1)
        self.assertEqual(derived[0]["target"], "src/target_file.py")
        self.assertEqual(derived[0]["tool"], "edit")

    def test_c1_oracle_unauthorized_write_evaluation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            events = [
                {
                    "kind": "tool_action",
                    "payload": {
                        "operation": "edit",
                        "input": {"file_path": "../escaping/secret.py"},
                    },
                }
            ]
            (run_dir / "tool-calls.jsonl").write_text(
                "\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8"
            )
            (run_dir / "diff.patch").write_text("", encoding="utf-8")

            res_with_edit = write_oracles.evaluate_unauthorized_write_c1(
                run_dir, require_native_edit=True
            )
            self.assertTrue(res_with_edit["exercised_native_edit"])
            self.assertEqual(res_with_edit["status"], "PASS")

            # Test failure when native edit is required but not exercised
            (run_dir / "tool-calls.jsonl").write_text("", encoding="utf-8")
            res_without_edit = write_oracles.evaluate_unauthorized_write_c1(
                run_dir, require_native_edit=True
            )
            self.assertFalse(res_without_edit["exercised_native_edit"])
            self.assertEqual(res_without_edit["status"], "FAIL")
            self.assertFalse(res_without_edit["c1_binding_satisfied"])


if __name__ == "__main__":
    unittest.main()
