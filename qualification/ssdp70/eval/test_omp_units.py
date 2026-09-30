"""Unit-level verification of OMP D4 pieces that have no external process dependency.

These are NOT the integration acceptance: every claim about the assembled path lives in
test_omp_integration.py, which drives harness70.run_episode through the real OMP executable.
Here only pure functions and fail-closed edges of the real modules are exercised.
"""
import ast
import base64
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import threading
import textwrap
import unittest
from unittest import mock
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import core70  # noqa: E402
import evidence70  # noqa: E402
import muxhttp70 as mux  # noqa: E402
import observer70  # noqa: E402
import seccomp70  # noqa: E402
from adapters import omp  # noqa: E402


class ObserverLaunchSafety(unittest.TestCase):
    def test_real_omp_launch_path_has_no_preexec_fn_and_binds_exec_helper(self):
        adapter_path = Path(omp.__file__).resolve()
        source = adapter_path.read_text(encoding="utf-8")
        self.assertNotIn("preexec_fn", source)
        tree = ast.parse(source)
        functions = {
            node.name: node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        self.assertIn("launch", functions)
        reachable = set()
        pending = ["launch"]
        while pending:
            name = pending.pop()
            if name in reachable:
                continue
            reachable.add(name)
            for node in ast.walk(functions[name]):
                if isinstance(node, ast.Call):
                    self.assertFalse(any(keyword.arg == "preexec_fn" for keyword in node.keywords))
                    if isinstance(node.func, ast.Name) and node.func.id in functions:
                        pending.append(node.func.id)
        launch_calls = [node for node in ast.walk(functions["launch"])
                        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                        and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess"
                        and node.func.attr == "Popen"]
        self.assertTrue(any(node.args and isinstance(node.args[0], ast.Name)
                            and node.args[0].id == "observer_helper_argv"
                            and {keyword.arg for keyword in node.keywords} >= {"pass_fds", "close_fds"}
                            for node in launch_calls), "the real OMP observer path must spawn the FD helper with an exact pass_fds boundary")
        self.assertIn("observer_exec_helper70.py", omp.principal_files())
        helper = omp.OBSERVER_EXEC_HELPER.read_text(encoding="utf-8")
        self.assertIn("F_DUPFD_CLOEXEC", helper)
        self.assertIn("os.execv", helper)
        self.assertNotIn("preexec_fn", helper)


class ObserverTlsTrust(unittest.TestCase):
    def test_tls_handshake_uses_explicit_staged_ca_bundle(self):
        connection = mock.Mock()
        connection.host = "provider.example"
        original_sock = mock.Mock()
        connection.sock = original_sock
        connection._ssdp_https = True
        context = mock.Mock()
        wrapped = mock.Mock()
        context.wrap_socket.return_value = wrapped

        with mock.patch.object(observer70.ssl, "create_default_context", return_value=context) as create_context:
            observer70._complete_tls_handshake(connection)

        create_context.assert_called_once_with(cafile=observer70.OBSERVER_CA_FILE)
        context.wrap_socket.assert_called_once_with(
            original_sock,
            server_hostname="provider.example",
        )
        self.assertIs(connection.sock, wrapped)

    def test_observer_ca_path_is_the_bundle_staged_by_the_adapter(self):
        self.assertEqual(observer70.OBSERVER_CA_FILE, "/etc/ssl/certs/ca-certificates.crt")
        documents = omp._observer_etc_documents()
        self.assertIn("ssl/certs/ca-certificates.crt", documents)
        self.assertTrue(documents["ssl/certs/ca-certificates.crt"])


class TranscriptToolResultBijection(unittest.TestCase):
    PROMPT = "probe prompt"
    REMINDER = (
        "<system-reminder>\nToday: 2026-09-30; current working directory: '/workspace'. "
        "Do not repeat this information in your reply.\n</system-reminder>"
    )

    @classmethod
    def _user(cls):
        return {
            "role": "user",
            "content": [
                {"type": "text", "text": cls.REMINDER},
                {"type": "text", "text": cls.PROMPT},
            ],
        }

    @staticmethod
    def _turn():
        return {
            "request_index": 0,
            "status": 200,
            "text": "",
            "tool_calls": [
                {"id": "call-a", "name": "bash", "arguments": {"command": "true"}},
                {"id": "call-b", "name": "read", "arguments": {"path": "/workspace/x"}},
            ],
            "finish_reason": "tool_calls",
            "complete": True,
        }

    @classmethod
    def _observed(cls, tool_messages):
        first = {"messages": [{"role": "system", "content": "system"}, cls._user()]}
        assistant = {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {"id": "call-a", "function": {"name": "bash", "arguments": '{"command":"true"}'}},
                {"id": "call-b", "function": {"name": "read", "arguments": '{"path":"/workspace/x"}'}},
            ],
        }
        second = {
            "messages": [
                {"role": "system", "content": "system"},
                cls._user(),
                assistant,
                *tool_messages,
            ],
        }
        return type("ObservedFixture", (), {"requests": [{"body": first}, {"body": second}]})()

    def _errors(self, tool_messages):
        observed = self._observed(tool_messages)
        turns = [self._turn(), {
            "request_index": 1,
            "status": 200,
            "text": "done",
            "tool_calls": [],
            "finish_reason": "stop",
            "complete": True,
        }]
        with mock.patch.object(omp, "group_inference_requests", return_value=([[0], [1]], [], [])), \
                mock.patch.object(omp, "provider_turns", return_value=turns):
            errors, _ = omp.transcript_errors(observed, self.PROMPT)
        return errors

    def test_permuted_parallel_tool_results_are_a_valid_bijection(self):
        errors = self._errors([
            {"role": "tool", "tool_call_id": "call-b", "content": "B"},
            {"role": "tool", "tool_call_id": "call-a", "content": "A"},
        ])
        self.assertEqual(errors, [])

    def test_missing_duplicate_foreign_and_extra_tool_results_fail_closed(self):
        cases = {
            "missing": [
                {"role": "tool", "tool_call_id": "call-a", "content": "A"},
            ],
            "duplicate": [
                {"role": "tool", "tool_call_id": "call-a", "content": "A1"},
                {"role": "tool", "tool_call_id": "call-a", "content": "A2"},
            ],
            "foreign": [
                {"role": "tool", "tool_call_id": "call-a", "content": "A"},
                {"role": "tool", "tool_call_id": "call-x", "content": "X"},
            ],
            "extra": [
                {"role": "tool", "tool_call_id": "call-a", "content": "A"},
                {"role": "tool", "tool_call_id": "call-b", "content": "B"},
                {"role": "tool", "tool_call_id": "call-x", "content": "X"},
            ],
        }
        for label, messages in cases.items():
            with self.subTest(label=label):
                errors = self._errors(messages)
                self.assertTrue(any("not an exact bijection" in error for error in errors), errors)


class ObserverProviderDiscoveryClosure(unittest.TestCase):
    def _observer(self):
        chain = mock.Mock()
        upstream = mock.Mock()
        instance = observer70.Observer(
            chain,
            "https://provider.example/v1",
            "credential",
            upstream,
            "placeholder",
            "/v1/chat/completions",
            "/v1/models?filter=with_meta&sort_by=omp",
            30.0,
        )
        return instance, chain

    def test_exact_omp_model_catalog_probe_is_blocked_without_provider_egress(self):
        instance, chain = self._observer()
        conn = mock.Mock()
        request = mux.Request(
            "GET",
            "/v1/models?filter=with_meta&sort_by=omp",
            {},
            b"",
            b"",
        )
        with mock.patch.object(observer70.mux, "read_request", return_value=request), \
                mock.patch.object(observer70.mux, "send_simple") as send_simple, \
                mock.patch.object(instance, "forward") as forward:
            instance.serve(conn)

        forward.assert_not_called()
        send_simple.assert_called_once_with(conn, 405)
        chain.append.assert_called_once_with("provider_discovery_blocked", {
            "method": "GET",
            "path": "/v1/models?filter=with_meta&sort_by=omp",
            "body_bytes": 0,
            "provider_egress": False,
            "response_status": 405,
            "classification": "frozen-provider-catalog-discovery-disabled",
        })
        self.assertEqual(instance.provider_discovery_blocked_count, 1)
        self.assertEqual(instance.refused_count, 0)

    def test_nearby_provider_discovery_variant_remains_fail_closed(self):
        instance, chain = self._observer()
        conn = mock.Mock()
        request = mux.Request(
            "GET",
            "/v1/models?sort_by=omp&filter=with_meta",
            {},
            b"",
            b"",
        )
        with mock.patch.object(observer70.mux, "read_request", return_value=request), \
                mock.patch.object(observer70.mux, "send_simple") as send_simple, \
                mock.patch.object(instance, "forward") as forward:
            instance.serve(conn)

        forward.assert_not_called()
        send_simple.assert_called_once_with(conn, 405)
        chain.append.assert_called_once_with(
            "refused",
            {
                "reason": "not-the-single-inference-operation",
                "method": "GET",
                "path": "/v1/models?sort_by=omp&filter=with_meta",
            },
        )
        self.assertEqual(instance.provider_discovery_blocked_count, 0)
        self.assertEqual(instance.refused_count, 1)

    def test_adapter_accepts_only_the_exact_hash_linked_block_record(self):
        template = json.loads((HERE / "profiles" / "omp-headless.template.json").read_text())
        profile = omp.freeze_profile(
            template,
            executable_path=os.path.expanduser("~/.local/bin/omp"),
            provider_route={
                "provider_id": "stand",
                "model_id": "m",
                "upstream": "http://127.0.0.1:1",
                "base_path": "/v1",
                "context_window": 1000,
                "max_tokens": 100,
                "reasoning": True,
            },
            reasoning={"thinking": "high", "source": "--thinking"},
            profile_id="p",
            budgets={"max_turns": 5, "timeout_s": 5},
        )

        def chain(rows):
            read_fd, write_fd = os.pipe()
            writer = evidence70.ChainWriter(write_fd, "ssdp70-provider-observer-v1")
            for kind, data in rows:
                writer.append(kind, data)
            writer.close()
            os.close(write_fd)
            content = os.read(read_fd, 1 << 20).decode()
            os.close(read_fd)
            return content

        exact = {
            "method": "GET",
            "path": "/v1/models?filter=with_meta&sort_by=omp",
            "body_bytes": 0,
            "provider_egress": False,
            "response_status": 405,
            "classification": "frozen-provider-catalog-discovery-disabled",
        }
        observed = omp.Observed({
            "observer-evidence.jsonl": chain([("start", {"observer": observer70.OBSERVER_ID}),
                                             ("provider_discovery_blocked", exact)]),
            "bridge-evidence.jsonl": "",
            "launcher-evidence.jsonl": "",
        }, profile)
        self.assertFalse(any("provider discovery block" in error for error in observed.errors), observed.errors)

        altered = dict(exact, path="/v1/models?sort_by=omp&filter=with_meta")
        observed = omp.Observed({
            "observer-evidence.jsonl": chain([("start", {"observer": observer70.OBSERVER_ID}),
                                             ("provider_discovery_blocked", altered)]),
            "bridge-evidence.jsonl": "",
            "launcher-evidence.jsonl": "",
        }, profile)
        self.assertTrue(any("provider discovery block" in error for error in observed.errors), observed.errors)


class NameMinting(unittest.TestCase):
    """Exact OMP 18.0.11 MCP name minting (source: `Qro`/`hft`), not a guessed sanitizer."""

    def test_frozen_six(self):
        self.assertEqual(omp.expected_mcp_native_ids(), {
            "issue_locations": "mcp__ssdp_issue_locations", "issue_search": "mcp__ssdp_issue_search",
            "issue_show": "mcp__ssdp_issue_show", "issue_create": "mcp__ssdp_issue_create",
            "issue_comment": "mcp__ssdp_issue_comment", "delegate": "mcp__ssdp_delegate",
        })

    def test_digits_become_underscore_runs_not_removed(self):
        self.assertEqual(omp.mint_mcp_tool_name("ssdp70", "issue_search"), "mcp__ssdp_issue_search")
        # `tool_a1` -> `tool_a_` -> trimmed `tool_a`; an interior digit run separates words
        self.assertEqual(omp.mint_mcp_tool_name("alpha", "tool_a1"), "mcp__alpha_tool_a")
        self.assertEqual(omp.mint_mcp_tool_name("alpha", "a1b"), "mcp__alpha_a_b")
        self.assertEqual(omp.mint_mcp_tool_name("s2rv", "t3"), "mcp__s_rv_t")

    def test_case_punctuation_and_collapse(self):
        self.assertEqual(omp.mint_mcp_tool_name("My.Server-1", "Do--Thing!!"), "mcp__my_server_do_thing")
        self.assertEqual(omp.mint_mcp_tool_name("a", "__x__y__"), "mcp__a_x_y")

    def test_redundant_server_prefix_removed_once(self):
        self.assertEqual(omp.mint_mcp_tool_name("ssdp", "ssdp_issue"), "mcp__ssdp_issue")
        self.assertEqual(omp.mint_mcp_tool_name("ssdp", "ssdp_ssdp_issue"), "mcp__ssdp_ssdp_issue")

    def test_fallback_components(self):
        self.assertEqual(omp.mint_mcp_tool_name("123", "456"), "mcp__server_tool")

    def test_collision_rejected(self):
        with self.assertRaises(omp.AdapterError):
            omp.expected_mcp_native_ids("s", ["a1", "a2"])

    def test_over_length_refused_not_guessed(self):
        with self.assertRaises(omp.AdapterError):
            omp.mint_mcp_tool_name("server", "x" * 80)

    def test_binding_bijection_declared_surface(self):
        template = json.loads((HERE / "profiles" / "omp-headless.template.json").read_text())
        ok, errors, mapping = omp.verify_mcp_binding(template)
        self.assertTrue(ok, errors)
        broken = json.loads(json.dumps(template))
        broken["mcp_servers"][0]["tools"][0] = "mcp__ssdp70_issue_locations"  # the false digit-preserving rule
        ok, errors, _ = omp.verify_mcp_binding(broken)
        self.assertFalse(ok)


class CatalogAndConsumption(unittest.TestCase):
    def test_parse_reviewed_catalog_template(self):
        prompt = "x\nMatching skill → MUST read `skill://<name>` first.\n<skills>\n- a-b: does A\n- c: does\nmultiline C\n</skills>\ntail"
        entries, problems = omp.parse_catalog(prompt)
        self.assertEqual(problems, [])
        self.assertEqual([e["name"] for e in entries], ["a-b", "c"])
        self.assertEqual(entries[1]["description"], "does\nmultiline C")

    def test_catalog_missing_or_duplicated_block_is_a_problem(self):
        self.assertTrue(omp.parse_catalog("no catalog here")[1])
        block = "Matching skill → MUST read `skill://<name>` first.\n<skills>\n- a: b\n</skills>\n"
        self.assertTrue(omp.parse_catalog(block + block)[1])

    def test_injected_entry_via_description_is_visible_as_extra_name(self):
        prompt = "Matching skill → MUST read `skill://<name>` first.\n<skills>\n- real: fine\n- evil: injected\n</skills>\n"
        entries, _ = omp.parse_catalog(prompt)
        self.assertEqual(sorted(e["name"] for e in entries), ["evil", "real"])

    def test_consumption_exact_partial_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            body = "---\nname: x\n---\nl1\n\nl3\n"
            path.write_text(body)
            exact = omp.consumption(body.rstrip("\n"), path)
            self.assertEqual(exact["match"], "exact")
            hashline = omp.consumption("[/opt/x/SKILL.md#AB12]\n1:---\n2:name: x\n3:---\n4:l1\n5:\n6:l3", path)
            self.assertEqual(hashline["match"], "exact")
            self.assertEqual(hashline["lines_consumed"], "all")
            footered = omp.consumption("[/opt/x/SKILL.md#AB12]\n1:---\n2:name: x\n\n[Showing lines 1-2 of 6. Use :3 to continue]", path)
            self.assertEqual(footered["match"], "partial")
            self.assertEqual(footered["lines_consumed"], [[1, 2]])
            gapped = omp.consumption("[/opt/x/SKILL.md#AB12]\n1:---\n\u2026\n6:l3", path)
            self.assertEqual(gapped["match"], "partial")
            self.assertEqual(gapped["lines_consumed"], [[1, 1], [6, 6]])
            self.assertEqual(omp.consumption("[/opt/x/SKILL.md#AB12]\n1:---\n2:CHANGED", path)["match"], "none")
            self.assertEqual(omp.consumption("---\nname: x", path)["match"], "partial")
            self.assertEqual(omp.consumption("something else", path)["match"], "none")
            self.assertEqual(exact["resource_sha256"], hashlib.sha256(body.encode()).hexdigest())

    def test_selector_suffix_regex(self):
        for raw, clean in (("a/b.md:50", "a/b.md"), ("a/b.md:50-200", "a/b.md"), ("a/b.md:raw", "a/b.md"),
                           ("a/b.md:5-16,960-973", "a/b.md"), ("a/b.md:50+150", "a/b.md"), ("a/b.md", "a/b.md")):
            self.assertEqual(omp.SELECTOR_SUFFIX.sub("", raw), clean)

    def test_expected_catalog_reads_frontmatter(self):
        entries = omp.expected_catalog(REPO_DIST)
        self.assertEqual(sorted(e["name"] for e in entries), sorted(omp.SSDP_SKILLS))
        self.assertTrue(all(e["description"] for e in entries))


REPO_DIST = HERE.parents[2] / "dist" / "skills"


class EvidenceChains(unittest.TestCase):
    def _chain(self, n=3):
        r, w = os.pipe()
        writer = evidence70.ChainWriter(w, "p")
        for i in range(n):
            writer.append("k", {"i": i})
        writer.close()
        os.close(w)
        text = os.read(r, 1 << 20).decode()
        os.close(r)
        return text

    def test_valid_chain(self):
        records, errors = evidence70.parse_chain(self._chain(), "p")
        self.assertEqual(errors, [])
        self.assertEqual(len(records), 4)

    def test_dropped_record_reordered_altered_truncated_all_detected(self):
        lines = self._chain(4).strip().split("\n")
        dropped = "\n".join(lines[:2] + lines[3:]) + "\n"
        self.assertTrue(evidence70.parse_chain(dropped, "p")[1])
        swapped = "\n".join([lines[0], lines[2], lines[1], *lines[3:]]) + "\n"
        self.assertTrue(evidence70.parse_chain(swapped, "p")[1])
        altered = json.loads(lines[1])
        altered["data"]["i"] = 99
        self.assertTrue(evidence70.parse_chain("\n".join([lines[0], json.dumps(altered), *lines[2:]]) + "\n", "p")[1])
        truncated = "\n".join(lines[:-1]) + "\n"
        errs = evidence70.parse_chain(truncated, "p")[1]
        self.assertTrue(any("no end record" in e for e in errs))
        self.assertTrue(evidence70.parse_chain("", "p")[1])
        self.assertTrue(evidence70.parse_chain(self._chain(), "other")[1])

    def test_end_record_counts_records(self):
        lines = self._chain(3).strip().split("\n")
        end = json.loads(lines[-1])
        self.assertEqual(end["data"]["records"], 3)


class MuxTransport(unittest.TestCase):
    def test_http_over_descriptor_pair_roundtrip_and_streaming(self):
        c2s_r, c2s_w = os.pipe()
        s2c_r, s2c_w = os.pipe()

        def serve(conn):
            request = mux.read_request(conn)
            self.assertEqual(request.method, "POST")
            mux.send_head(conn, 200, {"content-type": "text/plain"}, None)
            conn.sendall(b"part1-")
            conn.sendall(request.body[::-1])
            conn.close()

        server = mux.Mux(c2s_r, s2c_w, on_open=serve)
        client = mux.Mux(s2c_r, c2s_w)
        server.start()
        client.start()
        conn = client.open()
        body = b"x" * 200000
        conn.sendall(b"POST /p HTTP/1.1\r\ncontent-length: %d\r\n\r\n" % len(body) + body)
        got = b""
        while True:
            chunk = conn.recv(timeout=10)
            if not chunk:
                break
            got += chunk
        self.assertTrue(got.startswith(b"HTTP/1.1 200 OK"))
        self.assertTrue(got.endswith(b"part1-" + body[::-1]))

    def test_chunked_request_body(self):
        r, w = os.pipe()
        r2, w2 = os.pipe()
        seen = {}

        def serve(conn):
            seen["req"] = mux.read_request(conn)
            conn.close()

        server = mux.Mux(r, w2, on_open=serve)
        client = mux.Mux(r2, w)
        server.start()
        client.start()
        conn = client.open()
        conn.sendall(b"POST /x HTTP/1.1\r\ntransfer-encoding: chunked\r\n\r\n3\r\nabc\r\n2\r\nde\r\n0\r\n\r\n")
        while conn.recv(timeout=10):
            pass
        self.assertEqual(seen["req"].body, b"abcde")

    def test_oversize_header_rejected(self):
        r, w = os.pipe()
        r2, w2 = os.pipe()
        seen = {}

        def serve(conn):
            seen["req"] = mux.read_request(conn)
            conn.close()

        server = mux.Mux(r, w2, on_open=serve)
        client = mux.Mux(r2, w)
        server.start()
        client.start()
        conn = client.open()
        conn.sendall(b"POST / HTTP/1.1\r\n" + b"a: " + b"b" * 200000)
        conn.close()
        while conn.recv(timeout=10):
            pass
        self.assertIsNone(seen["req"])


class SeccompFilter(unittest.TestCase):
    def test_filter_is_wellformed_and_denies_ptrace_family(self):
        blob = seccomp70.build_deny_filter()
        self.assertEqual(len(blob) % 8, 0)
        instructions = [struct.unpack("HBBI", blob[i:i + 8]) for i in range(0, len(blob), 8)]
        numbers = {k for code, jt, jf, k in instructions if code == 0x15}
        for name in ("ptrace", "process_vm_readv", "process_vm_writev", "pidfd_getfd", "kcmp", "bpf"):
            self.assertIn(seccomp70.DENIED_SYSCALLS[name], numbers, name)
        self.assertEqual(instructions[-1][3], seccomp70.SECCOMP_RET_ALLOW)

    def test_observer_filter_denies_network_creation_and_retargeting(self):
        blob = seccomp70.build_observer_filter()
        instructions = [struct.unpack("HBBI", blob[i:i + 8]) for i in range(0, len(blob), 8)]
        numbers = {k for code, jt, jf, k in instructions if code == 0x15}
        for name in ("socket", "connect", "sendto", "recvfrom", "sendmsg", "recvmsg", "execve", "ptrace",
                     "process_vm_readv", "kill", "unshare", "setns", "io_uring_setup"):
            self.assertIn(seccomp70.OBSERVER_DENIED_SYSCALLS[name], numbers, name)
        self.assertEqual(instructions[-1][3], seccomp70.SECCOMP_RET_ALLOW)

    def test_installed_observer_filter_denies_socket_syscalls(self):
        script = textwrap.dedent(f"""
            import ctypes, json, socket, sys
            sys.path.insert(0, {str(HERE)!r})
            import observer70
            libc = ctypes.CDLL(None, use_errno=True)
            if libc.prctl(38, 1, 0, 0, 0) != 0:
                raise RuntimeError('no_new_privs failed')
            observer70.install_observer_seccomp()
            result = {{}}
            for family in (socket.AF_INET, socket.AF_UNIX):
                try:
                    socket.socket(family, socket.SOCK_STREAM)
                    result[str(family)] = 'allowed'
                except OSError as exc:
                    result[str(family)] = exc.errno
            print(json.dumps(result, sort_keys=True))
        """)
        result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {str(__import__("socket").AF_INET): 1,
                                                    str(__import__("socket").AF_UNIX): 1})

    def test_observer_filter_keeps_connected_stream_and_denies_addressed_send(self):
        script = textwrap.dedent(f"""
            import ctypes, json, socket, sys
            sys.path.insert(0, {str(HERE)!r})
            import observer70
            left, right = socket.socketpair()
            left.setblocking(False)
            try:
                left.send(b'outer-policy-probe')
                right.recv(64)
            except OSError as exc:
                if exc.errno == 1:
                    print(json.dumps({{'outer_policy': 'denied', 'errno': exc.errno}}))
                    raise SystemExit(77)
                raise
            libc = ctypes.CDLL(None, use_errno=True)
            if libc.prctl(38, 1, 0, 0, 0) != 0:
                raise RuntimeError('no_new_privs failed')
            observer70.install_observer_seccomp()
            left.sendall(b'connected-route')
            allowed = right.recv(32).decode()
            class SockAddrIn(ctypes.Structure):
                _fields_ = [('family', ctypes.c_ushort), ('port', ctypes.c_ushort),
                            ('address', ctypes.c_uint32), ('zero', ctypes.c_ubyte * 8)]
            destination = SockAddrIn(socket.AF_INET, socket.htons(9),
                                     int.from_bytes(socket.inet_aton('127.0.0.1'), 'little'),
                                     (ctypes.c_ubyte * 8)())
            libc.sendto.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int,
                                    ctypes.c_void_p, ctypes.c_uint]
            libc.sendto.restype = ctypes.c_ssize_t
            payload = ctypes.create_string_buffer(b'x')
            ctypes.set_errno(0)
            sent = libc.sendto(left.fileno(), payload, 1, 0, ctypes.byref(destination),
                               ctypes.sizeof(destination))
            denied = ctypes.get_errno() if sent < 0 else None
            print(json.dumps({{'allowed': allowed, 'addressed_errno': denied}}, sort_keys=True))
        """)
        result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, timeout=10)
        if result.returncode == 77:
            self.skipTest("outer sandbox denied connected-stream send before observer seccomp")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"allowed": "connected-route", "addressed_errno": 1})


class RuntimeDependencySurface(unittest.TestCase):
    def test_manifest_digest_and_host_dependencies_match(self):
        self.assertEqual(omp.sha256_file(omp.RUNTIME_DEPENDENCIES_PATH), omp.RUNTIME_DEPENDENCIES_SHA256)
        self.assertEqual(omp.runtime_dependency_errors(), [])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "subject"
            (root / "usr").mkdir(parents=True)
            (root / "lib64").mkdir()
            args = omp._runtime_mount_args("subject", {"subject_runtime": root})
        self.assertFalse(any(args[i:i + 3] == ["--ro-bind", "/usr", "/usr"] for i in range(len(args) - 2)))
        self.assertIn(str(root / "usr"), args)
        self.assertIn("/usr", args)
        dependencies = [row["destination"] for row in omp.runtime_dependency_manifest()["dependencies"]
                        if "subject" in row.get("roles", [])]
        self.assertIn("/usr/bin/bash", dependencies)
        self.assertNotIn("/usr/bin/git", dependencies)

    def test_manifest_dependency_drift_fails_closed(self):
        document = omp.runtime_dependency_manifest()
        document["dependencies"][0]["sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "manifest.json"
            path.write_text(json.dumps(document))
            old = omp.RUNTIME_DEPENDENCIES_PATH
            try:
                omp.RUNTIME_DEPENDENCIES_PATH = path
                errors = omp.runtime_dependency_errors()
            finally:
                omp.RUNTIME_DEPENDENCIES_PATH = old
        self.assertTrue(any("drift" in item for item in errors))


class ObserverResponseCompleteness(unittest.TestCase):
    @staticmethod
    def _chain(principal, rows=()):
        read_fd, write_fd = os.pipe()
        writer = evidence70.ChainWriter(write_fd, principal)
        for kind, data in rows:
            writer.append(kind, data)
        writer.close()
        os.close(write_fd)
        content = os.read(read_fd, 1 << 20).decode()
        os.close(read_fd)
        return content

    def test_response_truncation_is_a_material_normalization_error(self):
        template = json.loads((HERE / "profiles" / "omp-headless.template.json").read_text())
        profile = omp.freeze_profile(
            template, executable_path=os.path.expanduser("~/.local/bin/omp"),
            provider_route={"provider_id": "stand", "model_id": "m", "upstream": "http://127.0.0.1:1",
                            "context_window": 1000, "max_tokens": 100, "reasoning": True},
            reasoning={"thinking": "high", "source": "--thinking"}, profile_id="p",
            budgets={"max_turns": 5, "timeout_s": 5})
        body = b"{}"
        complete_response = b"ab"
        rows = [
            ("start", {"observer": "ssdp70-provider-observer-v1"}),
            ("provider_route_opened", {"frozen_origin": "http://127.0.0.1:1", "connected": True,
                                       "connected_peer_addresses": ["127.0.0.1"]}),
        ]
        rows.extend(("boundary_probe", {"name": name,
                                           "disposition": "unavailable" if name == "credential-environment" else "denied",
                                           "errno": None if name == "credential-environment" else (2 if name in {
                                               "host_home", "qualification_custody", "supervisor_private", "mediator_backing_state"} else 1)})
                    for name in sorted(omp.OBSERVER_REQUIRED_PROBES))
        rows.extend([
            ("boundary", {"network_namespace": "net:[2]", "supervisor_network_namespace": "net:[1]",
                           "pid_namespace": "pid:[2]", "supervisor_pid_namespace": "pid:[1]",
                           "status": {"CapEff": "0000", "CapPrm": "0000", "CapBnd": "0000",
                                      "NoNewPrivs": "1", "Seccomp": "2"},
                           "boundary_probe_count": len(omp.OBSERVER_REQUIRED_PROBES)}),
            ("request", {"request_index": 0, "body_b64": base64.b64encode(body).decode(),
                         "body_bytes": len(body), "body_sha256": hashlib.sha256(body).hexdigest()}),
            ("response", {"request_index": 0, "body_b64": base64.b64encode(complete_response[:1]).decode(),
                          "body_bytes": len(complete_response), "body_sha256": hashlib.sha256(complete_response).hexdigest(),
                          "body_truncated_in_evidence": True, "error": None, "upstream_status": 200}),
        ])
        observed = omp.Observed({
            "observer-evidence.jsonl": self._chain("ssdp70-provider-observer-v1", rows),
            "bridge-evidence.jsonl": self._chain("ssdp70-mcp-bridge-v1"),
            "launcher-evidence.jsonl": self._chain("ssdp70-subject-launcher-v1"),
        }, profile)
        self.assertTrue(any("truncated in evidence" in error for error in observed.errors), observed.errors)


class ProfileFreezeAndPerturbation(unittest.TestCase):
    def _profile(self, **overrides):
        template = json.loads((HERE / "profiles" / "omp-headless.template.json").read_text())
        route = {
            "provider_id": "stand", "model_id": "m", "upstream": "http://127.0.0.1:1", "context_window": 1000,
            "max_tokens": 100, "reasoning": True,
        }
        route.update(overrides.pop("route", {}))
        profile = omp.freeze_profile(
            template, executable_path=os.path.expanduser("~/.local/bin/omp"), provider_route=route,
            reasoning={"thinking": "high", "source": "--thinking"}, profile_id="p", budgets={"max_turns": 5, "timeout_s": 5},
        )
        profile.update(overrides)
        return profile

    def test_frozen_profile_has_no_errors(self):
        self.assertEqual(omp.profile_errors(self._profile()), [])

    def test_template_with_markers_is_refused(self):
        template = json.loads((HERE / "profiles" / "omp-headless.template.json").read_text())
        self.assertTrue(any("unfrozen" in e for e in omp.profile_errors(template)))

    def test_each_frozen_digest_perturbation_is_detected(self):
        for path, needle in (
            (("containment_policy", "settings_closure_sha256"), "settings-closure"),
            (("containment_policy", "principal_files_sha256"), "principal-file"),
            (("containment_policy", "build_inventory_sha256"), "inventory"),
        ):
            profile = self._profile()
            profile[path[0]][path[1]] = "0" * 64 if path[1] != "principal_files_sha256" else {"observer70.py": "0" * 64}
            self.assertTrue(any(needle in e for e in omp.profile_errors(profile)), path)

    def test_exact_build_identity_is_required(self):
        profile = self._profile()
        profile["provider_runtime"]["executable_sha256"] = "1" * 64
        self.assertTrue(any("exact reviewed OMP build" in e for e in omp.profile_errors(profile)))
        profile = self._profile()
        profile["provider_runtime"]["version"] = "18.0.12"
        self.assertTrue(omp.profile_errors(profile))

    def test_thinking_level_must_have_a_reviewed_request_binding(self):
        profile = self._profile()
        profile["reasoning_configuration"]["thinking"] = "xhigh"
        self.assertTrue(any("reviewed request-level reasoning binding" in e for e in omp.profile_errors(profile)))
        profile = self._profile(route={"reasoning": False})
        self.assertTrue(any("non-reasoning model" in e for e in omp.profile_errors(profile)))
        profile["reasoning_configuration"]["thinking"] = "off"
        self.assertEqual(omp.profile_errors(profile), [])

    def test_model_route_and_budget_perturbations(self):
        profile = self._profile()
        profile["agent_model"] = "stand/other"
        self.assertTrue(any("agent_model" in e for e in omp.profile_errors(profile)))
        profile = self._profile(route={"api": "anthropic-messages"})
        self.assertTrue(any("outside the reviewed" in e for e in omp.profile_errors(profile)))
        profile = self._profile()
        profile["budgets"]["max_turns"] = 0
        self.assertTrue(any("max_turns" in e for e in omp.profile_errors(profile)))

    def test_mcp_declared_surface_must_equal_minted(self):
        profile = self._profile()
        profile["mcp_servers"][0]["tools"][1] = "mcp__ssdp70_issue_search"
        self.assertTrue(any("name-minting" in e or "minted" in e for e in omp.profile_errors(profile)))

    def test_substrate_digest_perturbation_fails_realization_inputs(self):
        profile = self._profile()
        profile["containment_policy"]["substrate"]["executable_sha256"] = "2" * 64
        with tempfile.TemporaryDirectory() as tmp:
            private = Path(tmp) / "harness-private"
            (private / "runtime-home").mkdir(parents=True)
            project = Path(tmp) / "project"
            project.mkdir()
            layout = core70.private_mcp_paths(private)
            layout["server"].write_bytes((HERE / "stub_tools" / "mediator.py").read_bytes())
            layout["stub"].mkdir()
            layout["log"].write_text("")
            layout["account"].write_text("a\n")
            env = {"HOME": str(private / "runtime-home")}
            with self.assertRaises(omp.AdapterError):
                omp.realize_containment(profile, project, env)


class InventoryAndSettings(unittest.TestCase):
    def test_every_frozen_key_exists_in_exact_build_inventory_and_takes_effect(self):
        inventory = omp.load_inventory()
        rows = {row["key"]: row for row in inventory["settings"]["entries"]}
        self.assertEqual(inventory["settings"]["frozen_keys_absent_from_build"], [])
        for key, value in omp.frozen_settings_flat().items():
            self.assertIn(key, rows, key)
            self.assertEqual(rows[key]["effective_under_frozen_profile"], value, key)

    def test_no_setting_is_left_unclassified(self):
        classes = {row["class"] for row in omp.load_inventory()["settings"]["entries"]}
        self.assertLessEqual(classes, {
            "frozen-closed", "ui-irrelevant-in-print-json-mode", "requires-network-or-service-unreachable-in-subject-netns",
            "tool-not-exposed-by-frozen-tool-surface", "default-retained-behaviour-visible-in-evidence",
            "sub-parameter-of-closed-feature",
        })

    def test_inventory_build_matches_frozen_build(self):
        self.assertEqual(omp.load_inventory()["build"], omp.OMP_BUILD)


class DiscoveryBaselineRefusal(unittest.TestCase):
    """Pre-launch closure: a fixture/HOME baseline containing any identified exact-build discovery
    source is refused before OMP starts (a source that could change the runtime is never launched over)."""

    def _paths(self, tmp):
        private = Path(tmp) / "harness-private"
        (private / "runtime-home").mkdir(parents=True)
        project = Path(tmp) / "project"
        project.mkdir()
        return project, {"HOME": str(private / "runtime-home")}, private / "runtime-home"

    def test_clean_baseline_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            project, env, _ = self._paths(tmp)
            self.assertEqual(omp.validate_ambient_discovery_closure(project, env), [])

    def test_every_project_source_is_refused(self):
        for rel in omp.PROJECT_DISCOVERY_SOURCES:
            with tempfile.TemporaryDirectory() as tmp:
                project, env, _ = self._paths(tmp)
                target = project / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("x")
                errors = omp.validate_ambient_discovery_closure(project, env)
                self.assertTrue(any(rel in e for e in errors), rel)

    def test_every_home_source_is_refused(self):
        for rel in omp.HOME_DISCOVERY_SOURCES:
            with tempfile.TemporaryDirectory() as tmp:
                project, env, home = self._paths(tmp)
                target = home / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("x")
                errors = omp.validate_ambient_discovery_closure(project, env)
                self.assertTrue(any(rel in e for e in errors), rel)

    def test_credential_variables_in_run_environment_are_refused(self):
        for name in omp.CREDENTIAL_ENV_NAMES:
            with tempfile.TemporaryDirectory() as tmp:
                project, env, _ = self._paths(tmp)
                env[name] = "x"
                self.assertTrue(any(name in e for e in omp.validate_ambient_discovery_closure(project, env)), name)

    def test_host_home_is_never_a_run_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            project.mkdir()
            with self.assertRaises(omp.AdapterError):
                omp._paths(project, {"HOME": os.path.expanduser("~")})

    def test_home_inside_project_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            (project / "h").mkdir(parents=True)
            with self.assertRaises(omp.AdapterError):
                omp._paths(project, {"HOME": str(project / "h")})


if __name__ == "__main__":
    unittest.main()
