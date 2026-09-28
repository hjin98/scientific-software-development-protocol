import json
import tempfile
import unittest
from pathlib import Path

import core70
from adapters import claude


def write_json(path: Path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding='utf-8')


class PortableCoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.profile = self.root / 'profile.json'
        self.capabilities = self.root / 'capabilities.json'
        write_json(self.capabilities, {
            'schema': 1,
            'capabilities': {
                name: {'decision': 'ALLOW' if name not in {'delegation', 'network_remote_service'} else 'DENY', 'scope': '*'}
                for name in core70.REQUIRED_CAPABILITY_CLASSES
            },
        })
        write_json(self.profile, {
            'schema': 1,
            'profile_id': 'test-profile',
            'adapter_id': claude.ADAPTER_ID,
            'agent_model': 'test-model',
            'provider_runtime': {'provider': 'test', 'runtime': 'claude-code', 'executable': 'claude', 'version': 'exposed-v1'},
            'reasoning_configuration': {'effort': 'high'},
            'workspace_realization': {'kind': 'tempdir'},
            'install_mechanism': 'project-skills',
            'budgets': {'max_turns': 60, 'timeout_s': 3600},
            'containment_policy': {'kind': 'external-pre-effect'},
            'network_external_write_policy': {'network': 'deny', 'external_write': 'sandbox'},
            'credential_service_account_policy': {'ambient_credentials': 'deny'},
            'provider_managed_unknowns': [
                {'name': 'backend-shard', 'classification': 'arm-neutral', 'sensitive_claims': ['*']}
            ],
        })

    def tearDown(self):
        self.tmp.cleanup()

    def requirements(self):
        req = self.root / 'req'
        req.mkdir(exist_ok=True)
        write_json(req / 'required_artifacts.json', {'schema': 1, 'episodes': {'E1': ['final-report.md', 'trace.jsonl']}})
        write_json(req / 'required_oracles.json', {'schema': 1, 'episodes': {'E1': [{'id': 'o1', 'path': 'check_o1.py'}]}})
        write_json(req / 'expected_scoring_items.json', {'schema': 1, 'episodes': {'E1': [
            {'id': 'i1', 'measure': 'critical-judgment', 'critical': True, 'branch': 'main', 'allowed_dispositions': ['pass', 'fail', 'unresolved']},
            {'id': 'i2', 'measure': 'null-coverage', 'critical': False, 'branch': 'main', 'allowed_dispositions': ['pass', 'fail', 'unresolved', 'not-applicable']},
        ]}})
        return core70.load_requirements(req, 'E1')

    def test_profile_key_changes_with_material_capability_change(self):
        a = core70.load_profile(self.profile, self.capabilities)
        caps = json.loads(self.capabilities.read_text())
        caps['capabilities']['process_execution']['decision'] = 'DENY'
        write_json(self.capabilities, caps)
        b = core70.load_profile(self.profile, self.capabilities)
        self.assertNotEqual(a.profile_key_sha256, b.profile_key_sha256)

    def test_uncontrolled_provider_unknown_fails_sensitive_claim(self):
        profile = json.loads(self.profile.read_text())
        profile['provider_managed_unknowns'] = [
            {'name': 'hidden-system-prompt', 'classification': 'uncontrolled', 'sensitive_claims': ['owner-read']}
        ]
        write_json(self.profile, profile)
        bundle = core70.load_profile(self.profile, self.capabilities)
        self.assertTrue(core70.profile_claim_errors(bundle, ['owner-read']))
        self.assertFalse(core70.profile_claim_errors(bundle, ['timing']))

    def test_scoring_exact_closure_rejects_empty_and_duplicates(self):
        req = self.requirements()
        self.assertTrue(core70.validate_dispositions([], req))
        valid = [
            {'item': 'i1', 'measure': 'critical-judgment', 'critical': True, 'result': 'pass'},
            {'item': 'i2', 'measure': 'null-coverage', 'critical': False, 'result': 'not-applicable'},
        ]
        self.assertEqual(core70.validate_dispositions(valid, req), [])
        duplicate = valid + [dict(valid[0])]
        self.assertTrue(core70.validate_dispositions(duplicate, req))

    def test_required_artifact_and_oracle_fail_closed(self):
        req = self.requirements()
        run = self.root / 'run'
        run.mkdir()
        (run / 'final-report.md').write_text('x')
        missing = core70.validate_required_artifacts(run, req)
        self.assertEqual(missing, ['trace.jsonl'])
        self.assertEqual(core70.validate_required_oracles(run, req), ['o1'])
        (run / 'trace.jsonl').write_text('{}\n')
        (run / 'o1.out').write_text('ok')
        (run / 'o1.err').write_text('')
        write_json(run / 'oracle.json', {'schema': 1, 'results': {'o1': {
            'executed': True, 'stdout_artifact': 'o1.out', 'stderr_artifact': 'o1.err'
        }}})
        self.assertEqual(core70.validate_required_oracles(run, req), [])

    def test_normalization_completeness_rejects_dropped_event(self):
        events = [{
            'schema_version': 1, 'run_id': 'r', 'event_id': 'e000001', 'sequence': 1,
            'actor_id': 'executor', 'kind': 'termination', 'native_source': {'native_index': 1, 'native_sha256': 'a' * 64},
            'status': 'observed', 'timing': None, 'payload': {'terminal_result_exists': True}
        }]
        mapping = [{'native_index': 1, 'native_sha256': 'a' * 64, 'mapped_event_ids': ['e000001'], 'classification': 'terminal', 'oracle_relevant': True}]
        errors = core70.validate_completeness_map(2, mapping, events)
        self.assertTrue(any('missing from completeness map' in e for e in errors))

    def test_admission_binding_detects_stale_core_or_profile(self):
        bundle = core70.load_profile(self.profile, self.capabilities)
        admission = self.root / 'admission.json'
        write_json(admission, {
            'schema': 1,
            'status': 'ADMITTED',
            'profile_key_sha256': bundle.profile_key_sha256,
            'adapter_sha256': 'adapter-a',
            'core_sha256': 'core-a',
            'capability_manifest_sha256': bundle.capability_manifest_sha256,
            'checks': {'containment': True, 'normalization': True, 'scoring': True},
        })
        self.assertEqual(core70.validate_profile_admission(
            admission, mode='qualification', profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256='adapter-a', core_sha256='core-a', capability_manifest_sha256=bundle.capability_manifest_sha256,
        ), [])
        self.assertTrue(core70.validate_profile_admission(
            admission, mode='qualification', profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256='adapter-a', core_sha256='core-b', capability_manifest_sha256=bundle.capability_manifest_sha256,
        ))

    def test_normalized_event_order_must_match_native_order(self):
        events = [
            {'schema_version':1,'run_id':'r','event_id':'e1','sequence':1,'actor_id':'executor','kind':'resource_access',
             'native_source':{'native_index':1,'native_sha256':'a'*64},'status':'observed','timing':None,'payload':{}},
            {'schema_version':1,'run_id':'r','event_id':'e2','sequence':2,'actor_id':'executor','kind':'termination',
             'native_source':{'native_index':0,'native_sha256':'b'*64},'status':'observed','timing':None,'payload':{}},
        ]
        errors = core70.validate_normalized_events(events, 'r')
        self.assertTrue(any('reorder native event order' in e for e in errors))


class ClaudeAdapterTests(unittest.TestCase):
    def test_full_owner_read_is_not_truncated(self):
        long_prefix = 'x' * 1000
        stdout = '\n'.join([
            json.dumps({'type': 'system', 'subtype': 'init', 'skills': sorted(claude.SSDP_SKILLS), 'model': 'm'}),
            json.dumps({'type': 'assistant', 'message': {'content': [
                {'type': 'tool_use', 'name': 'Read', 'input': {'file_path': f'/tmp/{long_prefix}/scientific-inspectability-and-initiative.md'}}
            ]}}),
            json.dumps({'type': 'result', 'subtype': 'success', 'is_error': False, 'result': 'done', 'usage': {}}),
        ])
        events, mapping, errors, native_count = claude.normalize(stdout, 'run-1')
        self.assertEqual(errors, [])
        self.assertEqual(core70.validate_normalized_events(events, 'run-1'), [])
        self.assertEqual(core70.validate_completeness_map(native_count, mapping, events), [])
        self.assertTrue(claude.owner_reads(events, 'scientific-inspectability-and-initiative.md'))
        self.assertEqual(claude.final_result(events), 'done')

    def test_missing_terminal_event_is_observable(self):
        stdout = json.dumps({'type': 'system', 'subtype': 'init', 'skills': sorted(claude.SSDP_SKILLS)})
        events, mapping, errors, native_count = claude.normalize(stdout, 'run-2')
        self.assertEqual(errors, [])
        self.assertFalse(any(e['kind'] == 'termination' for e in events))
        self.assertEqual(core70.validate_completeness_map(native_count, mapping, events), [])

    def test_unknown_native_tool_is_fail_closed(self):
        stdout = json.dumps({'type': 'assistant', 'message': {'content': [
            {'type': 'tool_use', 'name': 'MagicTool', 'input': {'x': 1}}
        ]}})
        events, mapping, errors, native_count = claude.normalize(stdout, 'run-3')
        self.assertTrue(errors)
        self.assertEqual(core70.validate_completeness_map(native_count, mapping, events), [])



class EvidenceStateTests(unittest.TestCase):
    def test_incomplete_terminal_cannot_be_complete(self):
        state, reasons = core70.run_evidence_state(
            execution_ok=True, profile_errors=[], event_errors=[], completeness_errors=[],
            catalog_ok=True, terminal_exists=False, final_result_exists=False,
            missing_artifacts=[], missing_oracles=[])
        self.assertEqual(state, 'MISSING_REQUIRED_EVIDENCE')
        self.assertTrue(reasons)

    def test_execution_transport_success_does_not_override_inadmissible_profile(self):
        state, _ = core70.run_evidence_state(
            execution_ok=True, profile_errors=['uncontrolled hidden state'], event_errors=[], completeness_errors=[],
            catalog_ok=True, terminal_exists=True, final_result_exists=True,
            missing_artifacts=[], missing_oracles=[])
        self.assertEqual(state, 'INADMISSIBLE')

if __name__ == '__main__':
    unittest.main()
