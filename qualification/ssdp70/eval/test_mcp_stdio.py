import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERVER = HERE / "stub_tools" / "mediator.py"


class StdioMcpServerTests(unittest.TestCase):
    def prepare(self, root: Path):
        stub = root / "stub"
        issues = stub / "issues" / "main"
        delegates = stub / "delegates"
        issues.mkdir(parents=True)
        delegates.mkdir(parents=True)
        (stub / "issues" / "_config.json").write_text(
            json.dumps({"locations": {"main": "available", "archive": "unavailable"}}), encoding="utf-8"
        )
        (issues / "I-1.json").write_text(json.dumps({
            "title": "alpha anomaly", "body": "evidence", "labels": [], "comments": []
        }), encoding="utf-8")
        (delegates / "reviewer.json").write_text(json.dumps({"return": "delegate finding"}), encoding="utf-8")
        log = root / "side-effects.jsonl"
        log.write_text("", encoding="utf-8")
        account = root / "account.txt"
        account.write_text("agent\n", encoding="utf-8")
        return stub, log, account

    def run_server(self, requests):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            stub, log, account = self.prepare(root)
            sha = hashlib.sha256(SERVER.read_bytes()).hexdigest()
            proc = subprocess.run([
                sys.executable, str(SERVER),
                "--stub-root", str(stub),
                "--side-effect-log", str(log),
                "--account-file", str(account),
                "--server-id", "ssdp70-qualification-stdio-v1",
                "--expected-self-sha256", sha,
            ], input="\n".join(json.dumps(request) for request in requests) + "\n",
               capture_output=True, text=True, env={"PATH": str(Path(sys.executable).resolve().parent)})
            rows = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
            log_rows = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]
            return proc, rows, log_rows

    def test_initialize_tools_list_tools_call_protocol_smoke(self):
        requests = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                "protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}
            }},
            {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {
                "name": "issue_search", "arguments": {"query": "alpha"}
            }},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {
                "name": "issue_create", "arguments": {"location": "main", "title": "new", "body": "body", "labels": ["x"]}
            }},
            {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {
                "name": "delegate", "arguments": {"agent": "reviewer", "instruction": "inspect"}
            }},
        ]
        proc, rows, log_rows = self.run_server(requests)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(rows[0]["result"]["serverInfo"]["name"], "workspace-tools")
        names = [tool["name"] for tool in rows[1]["result"]["tools"]]
        self.assertEqual(names, [
            "issue_locations", "issue_search", "issue_show", "issue_create", "issue_comment", "delegate"
        ])
        search = json.loads(rows[2]["result"]["content"][0]["text"])
        created = json.loads(rows[3]["result"]["content"][0]["text"])
        delegated = json.loads(rows[4]["result"]["content"][0]["text"])
        self.assertEqual(search["evidence"]["object_ids"], ["I-1"])
        self.assertEqual(created["evidence"]["operation"], "create")
        self.assertTrue(created["evidence"]["after_object_version"])
        self.assertEqual(delegated["stdout"], "delegate finding\n")
        self.assertEqual([row["tool"] for row in log_rows], ["issues", "issues", "delegate"])

    def test_model_visible_surface_is_neutral_and_delegate_re_returns_frozen_content(self):
        """Contract A2/A3: no model-visible cue about scripting, stand-ins or qualification, except the
        adapter-pinned store identity; a repeated delegate call returns the same frozen content."""
        cues = ("script", "stub", "stand-in", "standin", "qualification", "ssdp", "frozen", "private", "stage f")
        delegate_call = lambda i: {"jsonrpc": "2.0", "id": i, "method": "tools/call", "params": {
            "name": "delegate", "arguments": {"agent": "reviewer", "instruction": "inspect"}}}
        requests = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                "protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "t", "version": "1"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            delegate_call(3), delegate_call(4),
            {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "issue_search", "arguments": {"query": "alpha"}}},
            {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "issue_show", "arguments": {"issue_id": "I-1"}}},
        ]
        proc, rows, _ = self.run_server(requests)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        init = rows[0]["result"]
        self.assertTrue(init["instructions"].strip(), "the adapter requires a present instructions string")
        visible = [init["instructions"], init["serverInfo"]["name"]]
        for tool in rows[1]["result"]["tools"]:
            visible += [tool["name"], tool["description"], json.dumps(tool["inputSchema"])]
        results = [json.loads(rows[i]["result"]["content"][0]["text"]) for i in (2, 3, 4, 5)]
        for result in results:
            self.assertEqual(result["evidence"].pop("store_identity"), "ssdp70-private-issue-standin")  # pinned residual
            visible += [json.dumps(result)]
        for text in visible:
            for cue in cues:
                self.assertNotIn(cue, text.lower(), f"model-visible text carries cue {cue!r}: {text[:80]!r}")
        self.assertNotIn("ssdp70-qualification-stdio-v1", init["instructions"])
        self.assertEqual(results[0]["stdout"], results[1]["stdout"])  # frozen re-return on every call
        self.assertEqual(results[0], results[1])

    def test_server_self_digest_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            stub, log, account = self.prepare(root)
            proc = subprocess.run([
                sys.executable, str(SERVER), "--stub-root", str(stub), "--side-effect-log", str(log),
                "--account-file", str(account), "--server-id", "ssdp70-qualification-stdio-v1",
                "--expected-self-sha256", "0" * 64,
            ], input="", capture_output=True, text=True, env={"PATH": str(Path(sys.executable).resolve().parent)})
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("digest mismatch", proc.stderr)


if __name__ == "__main__":
    unittest.main()
